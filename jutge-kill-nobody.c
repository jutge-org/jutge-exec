#include <unistd.h>
#include <signal.h>

// See https://lwn.net/Articles/754980/
int main() {
    // Uid 1015 is hardcoded.
    setresuid(1015, 65534, 1015);
    kill(-1, SIGKILL);
}