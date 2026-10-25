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
    goal='Üretilen tasarıma ve mağazanın KESİN ürün portföyüne uygun detaylı mockup promptları hazırlamak.',
    backstory='Görsel psikolojiyi kullanarak müşterinin ürünle bağ kurmasını sağlayan sanat yönetmeni. SADECE mağazanın stoğundaki ürünleri kullanır.',
    verbose=True
)

seo_ajani = Agent(
    role='SEO ve Raporlama Uzmanı',
    goal='Tüm ekibin ürettiği promptları ve SEO verilerini (Başlık, Etiket, Açıklama) tek bir düzgün rapor halinde sunmak.',
    backstory='Etsy algoritmasını bölgesel anahtar kelimelerle manipüle edebilen ve verileri mükemmel özetleyen pazarlamacı.',
    verbose=True
)

# MAĞAZA STRATEJİLERİ VE KESİN ÜRÜN PORTFÖYÜ
magazalar = [
    {
        "adi": "LoomifyTotes",
        "urun_tipleri": """SADECE şu 4 özel kanvas çanta modelinden biri seçilmelidir:
1) Two-Tone Elegance: Krem gövdeli, siyah tabanlı, siyah kanvas askılı ve askısında siyah-beyaz çizgili kurdele detayı olan şık çanta.
2) Rope Handle Beach Tote: Tamamen doğal krem rengi, kalın denizci halatı (rope) askılı çanta.
3) Tri-Color Block Tote: Üç yatay renk bloğundan oluşan (Üstü mavi/gri/pembe, ortası krem, altı koyu renk) ve standart kanvas askılı çanta.
4) Classic Zipper Canvas: Tamamen krem rengi, standart ince kanvas askılı, üstten fermuarlı klasik büyük çanta.""",
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
            description=f"Şu an {magaza['adi']} mağazası için çalışıyorsun. Satılan ürünler ve portföy: {magaza['urun_tipleri']}. Hedef Bölge/Kitle: {magaza['hedef_bolge']}. Bu dinamiklere uygun, bu hafta çok satacak 1 adet spesifik niş konu belirle.",
            expected_output='Detaylı trend niş konusu.',
            agent=arge_ajani
        )

        gorev2 = Task(
            description=f"Belirlenen niş için başka bir yapay zeka aracında (Midjourney vb.) kullanılmak üzere 1 adet yüksek kaliteli İngilizce ANA TASARIM PROMPTU hazırla. Tasarım şeffaf/temiz arka plana (isolated, solid clean background) sahip olmalıdır.",
            expected_output='Sadece İngilizce Ana Tasarım Promptu.',
            agent=tasarimci_ajan
        )

        gorev3 = Task(
            description=f"Belirlenen tasarıma en uygun ÜRÜNÜ seç ve mockup promptu yaz. EĞER mağaza LoomifyTotes ise, portföydeki 4 özel çanta modelinden tasarıma en uygun olan 1 tanesini seç (Örn: deniz/sahil tasarımıysa halat askılı, şehir modasıysa siyah tabanlı). Seçtiğin ürünün fiziksel özelliklerini (renk, askı tipi, kurdele vb.) mockup promptunun içine YEDİR (AI'nin o çantayı çizebilmesi için). 3 farklı İngilizce MOCKUP PROMPTU hazırla: 1. Kapak için Lifestyle Mockup (hedef bölgeye uygun arka plan). 2. Flatlay Mockup. 3. Detay (Macro) Mockup. Sadece bu 3 promptu liste halinde ver.",
            expected_output='3 adet mockup senaryosu içeren İngilizce prompt listesi.',
            agent=mockup_ajani
        )

        gorev4 = Task(
            description=f"Önceki ajanların ürettiği verileri topla. 1) Önerilen nişi ve eğer seçildiyse spesifik çanta modelini açıkla. 2) Tasarımcı ajanın yazdığı ANA TASARIM PROMPTU'nu ekle. 3) Mockup ajanının yazdığı 3 MOCKUP PROMPTU'nu ekle. 4) Son olarak bu listeleme için Etsy standartlarında 1 İngilizce başlık, 13 etiket (tags) ve ürün açıklaması (description) yaz. Tüm bunları Markdown formatında düzenli bir rapor olarak sun.",
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

{temiz_sonuc}

---
"""
        if github_summary:
            with open(github_summary, "a", encoding="utf-8") as f:
                f.write(rapor_metni)
                
    # GitHub Action çökmemesi için dummy dosya
    with open("ekrana_yaz.sh", "w", encoding="utf-8") as f:
        f.write("echo '✅ Tüm mağazaların işlemleri ve spesifik ürün prompt üretimleri tamamlandı.'")
        
    print("✅ Tüm mağazaların işlemleri başarıyla tamamlandı ve rapor oluşturuldu.")
