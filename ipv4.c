#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <unistd.h>
#include <errno.h>
#include <pthread.h>

#define MAX_PORTS 65535

struct Ipv4Address {
    char* ip;
};

struct ScanResult {
    int* ports;
    int count;
};

struct Ipv4Address* createIpv4Address(const char* ip) {
    struct Ipv4Address* address = malloc(sizeof(struct Ipv4Address));
    address->ip = strdup(ip);
    return address;
}

void destroyIpv4Address(struct Ipv4Address* address) {
    free(address->ip);
    free(address);
}

char** splitIp(struct Ipv4Address* address, const char* delimiter) {
    char* ipCopy = strdup(address->ip);
    char** parts = malloc(4 * sizeof(char*));
    int count = 0;

    char* token = strtok(ipCopy, delimiter);
    while (token != NULL && count < 4) {
        parts[count++] = strdup(token);
        token = strtok(NULL, delimiter);
    }

    free(ipCopy);

    return parts;
}

bool isValidIpv4Address(struct Ipv4Address* address) {
    char** parts = splitIp(address, ".");
    bool isValid = false;

    if (parts != NULL) {
        isValid = true;
        for (int i = 0; i < 4; i++) {
            int value = atoi(parts[i]);
            if (value < 0 || value > 255) {
                isValid = false;
                break;
            }
        }

        for (int i = 0; i < 4; i++) {
            free(parts[i]);
        }
        free(parts);
    }

    return isValid;
}

bool ipExists(struct Ipv4Address* address) {
    struct hostent* host = gethostbyname(address->ip);
    return (host != NULL);
}

struct ScanResult* scanPorts(struct Ipv4Address* address, int maxScanning, int timeout) {
    struct ScanResult* result = malloc(sizeof(struct ScanResult));
    result->ports = malloc(MAX_PORTS * sizeof(int));
    result->count = 0;

    struct timeval tv;
    tv.tv_sec = timeout;
    tv.tv_usec = 0;

    int sockfd;
    struct sockaddr_in server;
    struct hostent* host;

    host = gethostbyname(address->ip);

    if (host == NULL) {
        printf("Error: Failed to resolve hostname\n");
        result->count = -1;
        return result;
    }

    for (int port = 1; port <= MAX_PORTS; port++) {
        sockfd = socket(AF_INET, SOCK_STREAM, 0);
        if (sockfd < 0) {
            printf("Error: Failed to create socket\n");
            result->count = -1;
            return result;
        }

        server.sin_family = AF_INET;
        server.sin_port = htons(port);
        server.sin_addr = *((struct in_addr*)host->h_addr);
        bzero(&(server.sin_zero), 8);

        setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof(tv));

        if (connect(sockfd, (struct sockaddr*)&server, sizeof(struct sockaddr)) == 0) {
            result->ports[result->count++] = port;
        }

        close(sockfd);
    }

    return result;
}

bool isValidIp(const char* ip) {
    struct Ipv4Address* address = createIpv4Address(ip);
    bool
