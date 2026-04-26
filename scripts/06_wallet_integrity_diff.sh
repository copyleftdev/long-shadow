#!/usr/bin/env bash
# Section 9 of REPLAY.md — clone real upstreams and laundered, diff core wallet files.
set -e
WORK=${1:-/tmp/wallet-check}
mkdir -p $WORK
cd $WORK
[ -d zond-web3-wallet      ] || git clone --quiet https://github.com/theQRL/zond-web3-wallet.git
[ -d narwallets-extension  ] || git clone --quiet https://github.com/Narwallets/narwallets-extension.git
[ -d dimatura              ] || git clone --quiet https://github.com/luliguyu/dimatura.git
[ -d ssaavedrad            ] || git clone --quiet https://github.com/luliguyu/ssaavedrad.git

echo "=== Narwallets manifest version diff (laundered should be older = STALE) ==="
diff narwallets-extension/extension/manifest.json ssaavedrad/extension/manifest.json | head -10
echo
echo "=== Narwallets near-rpc.ts diff (RPC config — check for malicious endpoint changes) ==="
diff narwallets-extension/src/lib/near-api-lite/near-rpc.ts ssaavedrad/src/lib/near-api-lite/near-rpc.ts | head -20
echo
echo "=== QRL Zond file-level diff ==="
diff -rq --exclude=.git zond-web3-wallet dimatura | head -20
