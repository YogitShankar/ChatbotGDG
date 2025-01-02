#include <bits/stdc++.h>

using namespace std;

void solve() {
    int n; cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    
    long long ods = 0, evs = 0;
    for (int i = 0; i < n; i++) {
        if (i & 1) ods += a[i];
        else evs += a[i];
    }
    int odc = n / 2, evc = n / 2;
    if (n & 1) evc++;

    if (ods % odc != 0 || evs % evc != 0 || ods / odc != evs / evc) {
        cout << "NO";
        return;
    }
    cout << "YES";
}

int main() {
    int TESTS; cin >> TESTS;
    while (TESTS --> 0) {
        solve();
        cout << '\n';
    }
    return 0;
}