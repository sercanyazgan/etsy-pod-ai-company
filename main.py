import os
from crewai import Agent, Task, Crew, Process

# AJANLAR
arge_ajani = Agent(
    role='Etsy Pazar ve Bölge Stratejisti',
    goal='Verilen mağaza konseptine ve bölgesel hedeflere uygun, yüksek dönüşüm getirecek trend nişler bulmak.',
    backstory='Hedef kitle psikolojisini ve bölgesel satın alma alışkanlıklarını analiz eden e-ticaret dehası.',
    verbose=True
)

tasarimci_ajan = Agent(
    role='Kreatif Tasarım Direktörü',
    goal='Mağazanın ürün tipine uygun, Midjourney gibi yapay zeka araçlarında kullanılmak üzere mükemmel İngilizce görsel promptları yazmak.',
    backstory='Farklı materyallerin baskı dinamiklerini bilen ve prompt mühendisliğinde uzman yapay zeka tasarım direktörü.',
    verbose=True
)

mockup_ajani = Agent(
    role='Etsy Mockup ve Sunum Uzmanı',
    goal='Üretilen tasarıma ve ürün gamına uygun, listeleme kapağı ve diğer görseller için detaylı mockup promptları hazırlamak.',
    backstory='Görsel psikolojiyi kullanarak müşterinin ürünle bağ kurmasını sağlayan sanat yönetmeni.',
    verbose=True
)

seo_ajani = Agent(
    role='SEO ve Raporlama Uzmanı',
    goal='Tüm ekibin ürettiği promptları ve SEO verilerini (Başlık, Etiket, Açıklama) tek bir düzgün rapor halinde sunmak.',
    backstory='Etsy algoritmasını bölgesel anahtar kelimelerle manipüle edebilen ve verileri mükemmel özetleyen pazarlamacı.',
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
    
    if github_summary:
        with open(github_summary, "a", encoding="utf-8") as f:
            f.write("## 🏢 ETSY AJANSI GÜNLÜK ÜRETİM RAPORU\n\n")

    for magaza in magazalar:
        print(f"📁 Dosya Açılıyor: {magaza['adi']} Stratejisi İşleniyor...")
        
        # GÖREVLER
        gorev1 = Task(
            description=f"Şu an {magaza['adi']} mağazası için çalışıyorsun. Satılan ürünler: {magaza['urun_tipleri']}. Hedef Bölge/Kitle: {magaza['hedef_bolge']}. Bu dinamiklere uygun, bu hafta çok satacak 1 adet spesifik niş konu belirle.",
            expected_output='Detaylı trend niş konusu.',
            agent=arge_ajani
        )

        gorev2 = Task(
            description=f"Belirlenen niş ve '{magaza['urun_tipleri']}' ürünleri için başka bir yapay zeka aracında (Midjourney vb.) kullanılmak üzere 1 adet yüksek kaliteli İngilizce ANA TASARIM PROMPTU hazırla. Prompt, baskıya uygun olması için izole (isolated, clean solid background) detaylarını içermelidir.",
            expected_output='Sadece İngilizce Ana Tasarım Promptu.',
            agent=tasarimci_ajan
        )

        gorev3 = Task(
            description=f"Belirlenen tasarım için listelemede kullanılacak 3 farklı İngilizce MOCKUP PROMPTU hazırla: 1. Kapak görseli için Lifestyle Mockup Prompt (Hedef bölge olan '{magaza['hedef_bolge']}' ortamına uygun). 2. Flatlay Mockup Prompt. 3. Alternatif / Detay (Macro) Mockup Prompt. Sadece bu 3 promptu liste halinde ver.",
            expected_output='3 adet mockup senaryosu içeren İngilizce prompt listesi.',
            agent=mockup_ajani
        )

        gorev4 = Task(
            description=f"Önceki ajanların ürettiği verileri topla. 1) Önerilen nişi açıkla. 2) Tasarımcı ajanın yazdığı ANA TASARIM PROMPTU'nu ekle. 3) Mockup ajanının yazdığı 3 MOCKUP PROMPTU'nu ekle. 4) Son olarak bu ürün için Etsy standartlarında 1 İngilizce başlık, 13 etiket (tags) ve ürün açıklaması (description) yaz. Tüm bunları Markdown formatında düzenli bir rapor olarak sun.",
            expected_output='Ana prompt, mockup promptları ve SEO verilerini içeren düzenli Markdown raporu.',
            agent=seo_ajani
        )

        etsy_sirketi = Crew(
            agents=[arge_ajani, tasarimci_ajan, mockup_ajani, seo_ajani],
            tasks=[gorev1, gorev2, gorev3, gorev4],
            process=Process.sequential
        )
        
        sonuc = etsy_sirketi.kickoff()
        temiz_sonuc = str(sonuc).replace('"', '\\"')
        
        rapor_metni = f"""
### 🛍️ MAĞAZA: {magaza['adi']}
*Hedef Ürünler: {magaza['urun_tipleri']}*

{temiz_sonuc}

---
"""
        if github_summary:
            with open(github_summary, "a", encoding="utf-8") as f:
                f.write(rapor_metni)
                
    # GitHub Action çökmemesi için dummy dosya
    with open("ekrana_yaz.sh", "w", encoding="utf-8") as f:
        f.write("echo '✅ Tüm mağazaların işlemleri ve prompt üretimleri tamamlandı.'")
        
    print("✅ Tüm mağazaların işlemleri başarıyla tamamlandı ve rapor oluşturuldu.")
