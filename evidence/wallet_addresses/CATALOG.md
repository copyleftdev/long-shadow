# Crypto address catalog from laundered wallets (capture: 2026-04-25)

This catalog enumerates every cryptocurrency address found in the two laundered wallet repositories at the time of forensic capture. **All addresses match their upstreams — no malicious injections were detected.** The catalog exists so a future change to either repo can be diff-checked instantly: any address in either repo that is *not* in this catalog is a candidate operator-controlled address worth investigating immediately.

## QRL Zond wallet — `luliguyu/dimatura` (laundered) vs `theQRL/zond-web3-wallet` (upstream)

13 distinct Ethereum-style 0x-strings present in the laundered repo, all also present in upstream (mostly inside `src/.../__tests__/` test fixtures):

| Address | Identification | Source files (laundered) |
|---|---|---|
| `0x0db3981cb93db985e4e3a62ff695f7a1b242dd7c` | upstream test fixture (token-related) | `__tests__/TokenListItem.test.tsx`, `ZRC20Tokens.test.tsx`, `ImportToken.test.tsx`, etc. |
| `0x205046e6A6E159eD6ACedE46A36CAD6D449C80A1` | upstream test fixture (transaction recipient) | `GasFeeNotice.test.tsx` |
| `0x20D20b8026B8F02540246f58120ddAAf35AECD9B` | upstream test fixture | `ZondSendTransaction.test.tsx` |
| `0x20EE9760786AD48aB90E326c5cd78c6269Ba10AB` | upstream test fixture | `ZondSendTransaction*.test.tsx` |
| `0x20fB08fF1f1376A14C055E9F56df80563E16722b` | upstream test fixture | `GasFeeNotice.test.tsx` |
| `0x28c4113a9d3a2e836f28c23ed8e3c1e7c243f566` | upstream test fixture | `ZRC20Tokens.test.tsx`, `GasFeeNotice.test.tsx` |
| `0x5e4c1bd1e00d229fe4d72d64df0b2f20b7649a9e` | upstream test fixture | `TransactionSuccessful.test.tsx` |
| `0x6080604052348015600e575f5ffd5b5061012980` | EVM contract bytecode prefix (not an address) | `ZondSendTransaction*.test.tsx` |
| `0x641dcb99dfcd2ad3c3e7c3d30090b274b788a0f2` | upstream test fixture | `TransactionSuccessful.test.tsx` |
| `0x669e3a48fa068514e89bc2be248be964d22672cc` | upstream test fixture (mnemonic-derived seed test) | `getHexSeedFromMnemonic.test.ts`, `getMnemonicFromHexSeed.test.ts` |
| `0x7819dc0205e6a5c286796886ce16e637b99e1838` | upstream test fixture | `MnemonicDisplay.test.tsx` |
| `0x978918b7b544ad491d0b294cc6ac4d7bb0ef7112` | upstream test fixture | `ZRC20Tokens.test.tsx` |
| `0xd6921377489c736691d06ad610f105a5207f3d47` | upstream test fixture | `HexSeedListing.test.tsx` |

**Strings present in upstream but NOT in laundered** (laundered is older snapshot):
- `0x506c65617365207369676e2074686973206d6573` — hex-encoded ASCII *"Please sign this mes"*, a test signing-message string, not an address. In `PersonalSign.test.tsx` of upstream's `QrlWeb3Wallet/...` directory (which doesn't exist in laundered).
- `0xf86c0185174876e8008252089400000000000000` — RLP-encoded transaction prefix, not an address. Same upstream-only path.

**Verdict (capture date 2026-04-25): no operator-injected addresses.** All 0x-strings in the laundered repo are upstream-original test fixtures.

## NEAR Protocol — `luliguyu/ssaavedrad` (laundered) vs `Narwallets/narwallets-extension` (upstream)

15 distinct NEAR-format addresses, **all identical between laundered and upstream**:

| Address | Identification |
|---|---|
| `1f9840a85d5af5bf1d1762f925bdaddc4201f984.factory.bridge.near` | UNI (Uniswap ERC-20 token) bridged to NEAR |
| `2260fac5e5542a773aa44fbcfedf7c193bc2c599.factory.bridge.near` | WBTC (Wrapped Bitcoin) bridged to NEAR |
| `514910771af9ca656af840dff83e8264ecf986ca.factory.bridge.near` | LINK (Chainlink) bridged to NEAR |
| `6b175474e89094c44da98b954eedeac495271d0f.factory.bridge.near` | DAI (MakerDAO stablecoin) bridged to NEAR |
| `a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.factory.bridge.near` | USDC (Circle) bridged to NEAR |
| `dac17f958d2ee523a2206206994597c13d831ec7.factory.bridge.near` | USDT (Tether) bridged to NEAR |
| `f5cfbc74057c610c8ef151a439252680ac68c6dc.factory.bridge.near` | POND/Pool token bridged to NEAR |
| `berryclub.ek.near` | Berry Club NEAR-native token |
| `dbio.near` | DBIO NEAR-native token |
| `meta-pool.near` | Meta Pool (NEAR liquid-staking protocol) |
| `meta-token.near` | Meta Pool's META governance token |
| `token.paras.near` | Paras NFT marketplace token |
| `token.v2.ref-finance.near` | Ref Finance (NEAR DEX) token |
| `wrap.near` | wNEAR (wrapped NEAR token) |
| `xtoken.ref-finance.near` | xREF (Ref Finance staking token) |

These are **well-known mainnet token contracts** that any NEAR Protocol wallet UI needs to recognize. They are NOT operator-controlled — they're public token IDs hard-coded into the wallet's token-recognition logic.

**Verdict (capture date 2026-04-25): no operator-injected addresses.**

## Why a watcher is needed despite a clean snapshot

The operators (`luliguyu`, `countneurooman`) control both repos. Today's snapshot is benign. Tomorrow they could push:

- A modified `manifest.json` adding `"permissions": ["all_urls"]` for content-script injection
- A modified `near-rpc.ts` redirecting `https://rpc.mainnet.near.org` to an attacker-controlled proxy
- A modified `transaction.ts` swapping the receiver address before signing
- New 0x or `.near` addresses in the source not present in this catalog (operator wallets to receive drained funds)

The `tools/wallet_watcher.py` script periodically diffs each laundered wallet against:
1. The address allow-list in this CATALOG.md
2. The current upstream version (re-cloned each run)

It alerts on any address present in laundered that isn't allow-listed, on any change to wallet-critical files (`*.ts` files in `src/lib/`, `src/background/`, `manifest.json`, `near-rpc.ts`), and on any new file that doesn't exist in upstream.

Wallet-watcher data is in `data/wallet_watcher/state.json` after the first run.
