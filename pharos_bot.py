import os
from dotenv import load_dotenv
import requests
import time
from web3 import Web3
from datetime import datetime
import schedule

# Load environment variables
load_dotenv()

class PharosBot:
    def __init__(self):
        # Ambil private key dari .env
        self.private_key = os.getenv('PRIVATE_KEY')
        if not self.private_key:
            raise ValueError("❌ PRIVATE_KEY tidak ditemukan di file .env!")
        
        # Setting default
        self.rpc_url = os.getenv('RPC_URL', 'https://testnet-rpc.pharosnetwork.xyz')
        self.base_url = os.getenv('BASE_URL', 'https://testnet.pharosnetwork.xyz')
        
        # Setup Web3
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.account = self.w3.eth.account.from_key(self.private_key)
        self.address = self.account.address
        
        print(f"✅ Bot berhasil diinisialisasi untuk wallet: {self.address}")
    
    def daily_checkin(self):
        """Daily check-in function"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Content-Type': 'application/json'
            }
            
            checkin_data = {
                "address": self.address,
                "action": "daily_checkin",
                "timestamp": int(time.time())
            }
            
            response = requests.post(
                f"{self.base_url}/api/checkin",
                json=checkin_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ Daily check-in berhasil! - {datetime.now()}")
                return True
            else:
                print(f"❌ Daily check-in gagal: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error daily check-in: {str(e)}")
            return False
    
    def auto_swap(self, amount="0.01"):
        """Auto swap function"""
        try:
            swap_data = {
                "from_token": "ETH",
                "to_token": "USDT", 
                "amount": amount,
                "address": self.address
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                f"{self.base_url}/api/swap",
                json=swap_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ Auto swap berhasil! Amount: {amount} ETH")
                return True
            else:
                print(f"❌ Auto swap gagal: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error auto swap: {str(e)}")
            return False
    
    def run_daily_tasks(self):
        """Jalankan tugas harian"""
        print(f"\n🚀 Memulai tugas harian - {datetime.now()}")
        
        # Daily check-in
        self.daily_checkin()
        time.sleep(5)
        
        # Auto swap
        self.auto_swap()
        
        print("✅ Semua tugas harian selesai!\n")

def main():
    try:
        # Inisialisasi bot
        bot = PharosBot()
        
        # Jadwalkan tugas harian pada jam 9 pagi dan 9 malam
        schedule.every().day.at("09:00").do(bot.run_daily_tasks)
        schedule.every().day.at("21:00").do(bot.run_daily_tasks)
        
        print("🤖 Pharos Network Bot dimulai!")
        print("📅 Jadwal: 09:00 dan 21:00 setiap hari")
        print("⏹️  Tekan Ctrl+C untuk menghentikan bot\n")
        
        # Jalankan sekali saat startup
        bot.run_daily_tasks()
        
        # Loop utama
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check setiap menit
            
    except KeyboardInterrupt:
        print("\n🛑 Bot dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
