# include "sds.h"
# include "zmalloc.h"

sds     sdsnewlen(const void* init, size_t initlen) {
    struct sdshdr*  sh;

    sh = zmalloc(sizeof(struct sdshdr)+initlen+1);
    if (sh==NULL) return NULL;

    sh->len = initlen;
    sh->free = 0;
    if (initlen) {
        if (init) memcpy(sh->buf, init, initlen);
        else memset(sh->buf, 0, initlen);
    }
    sh->buf[initlen] = '\0';
    return (char*)sh->buf;
}

sds     sdsnew(const char* init) {
}

sds     sdsempty();
void    sdsfree(sds s);

size_t  sdslen(const sds s);
size_t  sdsavail(const sds s);

sds     sdsdup(const sds s);
// concat
sds     sdscatlen(sds s, void* t, size_t len);
sds     sdscat(sds s, char* t);
sds     sdscatprintf(sds s, const char* fmt, ...);

// copy and override
sds     sdscpylen(sds s, char* t, size_t len);
sds     sdscpy(sds s, char* t);

sds     sdstrim(sds s, const char* cset);
void    sdsupdatelen(sds s);
sds     sdsrange(sds s, long start, long end);

int     sdscmp(sds s1, sds s2);
sds*    sdssplitlen(char *s, int len, char *sep, int seplen, int* count);
void    sdstolower(sds s);
