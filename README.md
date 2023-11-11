<div align="center">
  <img src="https://i.imgur.com/XBGxKsN.png"  />
  <h1>Starknet Soft</h1>
  <p>A script designed to simplify your interaction with Starknet. It provides a wide range of features that will make it easier for you to work with Starknet, simplify the management of your farm, and allow you to perform a variety of operations on the network.</p>
</div>

---

🔔 <b>Автор основной версии:</b> https://t.me/sybilwave

---
<h2>🚀 Установка</h2>

```
git clone https://github.com/czbag/starknet.git

cd starknet

pip install -r requirements.txt

# Before you start, configure the required modules in modules_settings.py

python main.py
```
---
<h2> Updates </h2>

1. Private keys encryption
2. Logs saving
3. Gas sleep customization in main settings file

---
<h2>🚨 Modules</h2>

1. Make deposit/withdraw with official bridge (Does not work)

2. Make deposit/withdraw with Orbiter bridge (Does not work)

3. Swaps on JediSwap, MySwap, 10kSwap, SithSwap, Protoss, Avnu (avnu include ref system, 1% of the tx amount goes to me, come not from you, but from the Avnu contract! can be turned off in config.py)

4. Lending protocol zkLend(deposit/withdraw/enable_collateral)

5. Lending protocol Nostra (deposit/withdraw)

6. Mint Starknet ID

7. Mint StarkStars NFT

8. Dmail - email sender (onchain)

9. Transfer ETH to any wallets

10. Multi-swap capability - makes the specified number of swaps in the specified dexes

11. Custom routes - actions to be performed sequentially or randomly

12. Check gas before starting the module, if gas > specified, the software will wait for

13. Logging via logger module

14. Transaction count checker

---
<h2>⚙️ Настройка</h2>

1) All basic settings are made in settings.py and modules_settings.py, inside there is information about what and where to write

2) In the private_keys.txt file, specify your private keys

3) In the wallets.txt file, specify your wallet adresses (starknet)

4) In the recipients.txt file, specify you address (for withdraw with official bridge or orbiter)

5) In the rpc.json file at the path zksync/data/rpc.json we can change the rpc to ours

Info on updates and just a life blog –– https://t.me/sybilwave
