import os
from crewai import Agent, Task, Crew, Process
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def gorsel_uret(prompt_metni):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_metni,
            n=1,
            size="1024x1024",
            quality="hd"
        )
        return response.data.url
    except Exception as e:
        return f"Görsel üretilemedi: {str(e)}"

# 1. AJAN: Strateji ve Pazar Analizi
arge_ajani = Agent(
    role='Etsy Pazar ve Bölge Stratejisti',
    goal='Amerika satış haritasına göre LoomifyTotes (Bez Çanta) ve LoomifyGifts (Giyim) mağazaları için bölgesel trendleri analiz etmek.',
    backstory='Bölgesel satış verilerini (Midwest kamp kültürü, California Y2K/Brainrot trendleri, NY şehir hayatı vb.) ürün stratejisine dönüştüren uzman.',
    verbose=True
)

# 2. AJAN: Tasarım ve Kreatif
tasarimci_ajan = Agent(
    role='Kreatif Tasarım Direktörü',
    goal='Belirlenen mağaza ve bölge stratejisine uygun, basıma hazır (kanvas dokusu veya DTF hoodie) yüksek kaliteli görsel konseptleri üretmek.',
    backstory='Farklı materyallerin baskı dinamiklerini bilen ve hedef kitlenin görsel mizah anlayışına (GenZ, Midwest Nice vb.) hakim yapay zeka tasarım uzmanı.',
    verbose=True
)

# 3. AJAN: Sunum ve Mockup
mockup_ajani = Agent(
    role='Etsy Mockup ve Sunum Uzmanı',
    goal='Üretilen tasarıma ve hedef bölgenin kültürüne uygun (örn: NY kahve dükkanı, California sahili veya Midwest göl kenarı) mockup senaryoları hazırlamak.',
    backstory='Görsel psikolojiyi kullanarak müşterinin ürünle bağ kurmasını sağlayan ve dönüşüm oranlarını artıran sanat yönetmeni.',
    verbose=True
)

# 4. AJAN: SEO ve Metin
seo_ajani = Agent(
    role='SEO ve Listeleme Uzmanı',
    goal='Hedef bölgenin arama alışkanlıklarına ve kültürüne uygun İngilizce başlık, açıklama ve 13 adet niş etiket (tags) oluşturmak.',
    backstory='Etsy algoritmasını bölgesel anahtar kelimelerle (örn: midwest cozy hoodie, aesthetic canvas shopper) manipüle edebilen pazarlamacı.',
    verbose=True
)

# GÖREV 1: Strateji Belirleme
gorev1 = Task(
    description='Amerika satış haritamıza göre: Ya LoomifyTotes mağazası için (California/New York bölgesi, çevre bilinci, üniversite, tote bag) ya da LoomifyGifts mağazası için (Chicago/Midwest bölgesi, kalın kışlık giyim, kamp, doğa, lokal mizah) harika satacak 1 adet spesifik niş konu ve ürün türü belirle.',
    expected_output='Seçilen mağaza, hedef bölge ve detaylı trend niş konusu raporu.',
    agent=arge_ajani
)

# GÖREV 2: DALL-E Prompt Üretimi
gorev2 = Task(
    description="Belirlenen niş ve ürün türü (bez çanta veya hoodie) için DALL-E 3 promptu hazırla. Komut şunları içermelidir: 'Vibrant colors, clean solid background, isolated design, clean edges'. Yalnızca İngilizce prompt metnini çıktı olarak ver.",
    expected_output='DALL-E 3 için sadece İngilizce görsel promptu.',
    agent=tasarimci_ajan
)

# GÖREV 3: Mockup Prompt Üretimi
gorev3 = Task(
    description="Ana tasarıma ve hedef bölgenin ruhuna uygun 3 farklı mockup promptu hazırla: 1. Lifestyle model (bölgeye uygun arka planla). 2. Aesthetic flatlay. 3. Macro detay. Yalnızca İngilizce prompt metinlerini liste halinde ver.",
    expected_output='3 adet mockup senaryosu içeren İngilizce prompt listesi.',
    agent=mockup_ajani
)

# GÖREV 4: SEO Optimizasyonu
gorev4 = Task(
    description='Seçilen ürün ve hedef bölge için Etsy standartlarında 1 adet İngilizce başlık, 13 adet bölgesel trendlere uygun etiket ve SEO uyumlu ürün açıklaması yaz.',
    expected_output='Başlık, etiketler ve açıklama metni.',
    agent=seo_ajani
)

etsy_sirketi = Crew(
    agents=[arge_ajani, tasarimci_ajan, mockup_ajani, seo_ajani],
    tasks=[gorev1, gorev2, gorev3, gorev4],
    process=Process.sequential
)

if __name__ == "__main__":
    print("🚀 Yapay Zeka Şirketi Çalışmaya Başlıyor...")
    sonuc = etsy_sirketi.kickoff()
    
    print("🎨 Görsel Arka Planda Üretiliyor...")
    # Görsel komutunu otomatik alıp DALL-E'ye gönderiyoruz
    gorsel_linki = gorsel_uret(str(sonuc))
    
    # HATA ÇÖZÜMÜ: Çift tırnakları GitHub'ın okuyabileceği formata çeviriyoruz
    temiz_sonuc = str(sonuc).replace('"', '\\"')
    
    # Doğrudan GitHub paneline yazdırılacak Markdown rapor metni
    rapor_metni = f"""
### 📈 ETSY GÜNLÜK ÜRETİM RAPORU

#### 🎯 1. AR-GE & SEO SONUÇLARI
{temiz_sonuc}

#### 👕 2. ÜRETİLEN ANA TASARIM
[Tasarımı Yüksek Kalitede İndirmek İçin Tıklayın]({gorsel_linki})
"""
    
    # YÖNTEM DEĞİŞİKLİĞİ: Bash dosyası yerine doğrudan GitHub sistemine yazıyoruz (En güvenli yöntem)
    github_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if github_summary:
        with open(github_summary, "a", encoding="utf-8") as f:
            f.write(rapor_metni)
            
    # otomasyon.yml içindeki "Raporu Ekrana Kilitle" adımının hata vermemesi için boş dosya oluşturuyoruz
    with open("ekrana_yaz.sh", "w", encoding="utf-8") as f:
        f.write("echo '✅ İşlem tamamlandı, rapor Python tarafından başarıyla yazdırıldı.'")
        
    print("✅ Tüm işlemler başarıyla tamamlandı ve rapor oluşturuldu.")
