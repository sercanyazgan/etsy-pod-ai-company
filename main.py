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

# AJANLAR (Rolleri ve yetenekleri sabit olduğu için bir kez tanımlıyoruz)
arge_ajani = Agent(
    role='Etsy Pazar ve Bölge Stratejisti',
    goal='Verilen mağaza konseptine ve bölgesel hedeflere uygun, yüksek dönüşüm getirecek trend nişler bulmak.',
    backstory='Hedef kitle psikolojisini ve bölgesel satın alma alışkanlıklarını analiz eden e-ticaret dehası.',
    verbose=True
)

tasarimci_ajan = Agent(
    role='Kreatif Tasarım Direktörü',
    goal='Mağazanın ürün tipine (bez çanta veya giyim) uygun, basıma hazır yüksek kaliteli görsel konseptleri üretmek.',
    backstory='Farklı materyallerin baskı dinamiklerini bilen ve niş kitlelerin mizah/estetik anlayışına hakim yapay zeka tasarım uzmanı.',
    verbose=True
)

mockup_ajani = Agent(
    role='Etsy Mockup ve Sunum Uzmanı',
    goal='Üretilen tasarıma ve ürün gamına uygun mockup senaryoları hazırlamak.',
    backstory='Görsel psikolojiyi kullanarak müşterinin ürünle bağ kurmasını sağlayan sanat yönetmeni.',
    verbose=True
)

seo_ajani = Agent(
    role='SEO ve Listeleme Uzmanı',
    goal='Ürün tipine ve hedef bölgenin arama alışkanlıklarına uygun İngilizce başlık, açıklama ve 13 adet niş etiket oluşturmak.',
    backstory='Etsy algoritmasını bölgesel anahtar kelimelerle manipüle edebilen pazarlamacı.',
    verbose=True
)

# MAĞAZA STRATEJİLERİ
magazalar = [
    {
        "adi": "LoomifyTotes",
        "urun_tipleri": "Sadece Bez Çanta (Canvas Tote Bags)",
        "hedef_bolge": "California ve New York. Özellikler: Çevre bilinci, üniversite kültürü, şehir içi günlük kullanım, sahil modası, Y2K ve Gen Z mizahı."
    },
    {
        "adi": "LoomifyGifts",
        "urun_tipleri": "Toddler & Youth T-shirt, Adult T-shirt, Women Tank Top, Sweatshirt ve Hoodie",
        "hedef_bolge": "Midwest (Chicago ve Göller Bölgesi). Özellikler: Kamp, doğa, göl hayatı, lokal 'Midwest Nice' mizahı, rustik ve maskülen tasarımlar, soğuk iklim kışlık giyim."
    }
]

if __name__ == "__main__":
    print("🚀 Yapay Zeka Ajansı Çoklu Mağaza Yönetimi İçin Çalışmaya Başlıyor...\n")
    
    github_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    
    # Raporun başlığını bir kez yazdırıyoruz
    if github_summary:
        with open(github_summary, "a", encoding="utf-8") as f:
            f.write("## 🏢 ETSY AJANSI GÜNLÜK ÜRETİM RAPORU\n\n")

    # Her mağaza için ajansı sırayla çalıştırıyoruz
    for magaza in magazalar:
        print(f"📁 Dosya Açılıyor: {magaza['adi']} Stratejisi İşleniyor...")
        
        # GÖREVLER (Her mağazanın kendi dinamiklerine göre baştan tanımlanıyor)
        gorev1 = Task(
            description=f"Şu an {magaza['adi']} mağazası için çalışıyorsun. Satılan ürünler: {magaza['urun_tipleri']}. Hedef Bölge/Kitle: {magaza['hedef_bolge']}. Bu dinamiklere uygun, bu hafta çok satacak 1 adet spesifik niş konu belirle.",
            expected_output='Detaylı trend niş konusu raporu.',
            agent=arge_ajani
        )

        gorev2 = Task(
            description=f"Belirlenen niş ve '{magaza['urun_tipleri']}' ürünleri için DALL-E 3 promptu hazırla. Komut şunları içermelidir: 'Vibrant colors, clean solid background, isolated design, clean edges'. Yalnızca İngilizce prompt metnini çıktı olarak ver.",
            expected_output='DALL-E 3 için sadece İngilizce görsel promptu.',
            agent=tasarimci_ajan
        )

        gorev3 = Task(
            description=f"Ana tasarıma ve '{magaza['hedef_bolge']}' kültürüne uygun '{magaza['urun_tipleri']}' için 3 farklı mockup promptu hazırla (Lifestyle, Flatlay, Macro). Yalnızca İngilizce prompt metinlerini liste halinde ver.",
            expected_output='3 adet mockup senaryosu içeren İngilizce prompt listesi.',
            agent=mockup_ajani
        )

        gorev4 = Task(
            description=f"Seçilen ürün ({magaza['urun_tipleri']}) ve hedef bölge için Etsy standartlarında 1 adet İngilizce başlık, 13 adet etiket ve SEO uyumlu ürün açıklaması yaz.",
            expected_output='Başlık, etiketler ve açıklama metni.',
            agent=seo_ajani
        )

        # Ajans ekibini oluştur ve göreve başlat
        etsy_sirketi = Crew(
            agents=[arge_ajani, tasarimci_ajan, mockup_ajani, seo_ajani],
            tasks=[gorev1, gorev2, gorev3, gorev4],
            process=Process.sequential
        )
        
        sonuc = etsy_sirketi.kickoff()
        
        print(f"🎨 {magaza['adi']} için görsel üretiliyor...")
        gorsel_linki = gorsel_uret(str(sonuc))
        temiz_sonuc = str(sonuc).replace('"', '\\"')
        
        # Mağazaya özel rapor bloku
        rapor_metni = f"""
### 🛍️ MAĞAZA: {magaza['adi']}
*Hedef Ürünler: {magaza['urun_tipleri']}*

#### 🎯 AR-GE & SEO SONUÇLARI
{temiz_sonuc}

#### 👕 ÜRETİLEN ANA TASARIM
[Tasarımı Yüksek Kalitede İndirmek İçin Tıklayın]({gorsel_linki})

---
"""
        # Raporu GitHub paneline ekle
        if github_summary:
            with open(github_summary, "a", encoding="utf-8") as f:
                f.write(rapor_metni)
                
    # GitHub Action çökmemesi için dummy dosya
    with open("ekrana_yaz.sh", "w", encoding="utf-8") as f:
        f.write("echo '✅ Tüm mağazaların işlemleri tamamlandı.'")
        
    print("✅ Tüm mağazaların işlemleri başarıyla tamamlandı ve rapor oluşturuldu.")
