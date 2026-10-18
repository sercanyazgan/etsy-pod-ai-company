import os
from crewai import Agent, Task, Crew, Process

# 1. AJANLARIN TANIMLANMASI

# AR-GE Ajanı
arge_ajani = Agent(
    role='Etsy POD Trend Analisti',
    goal='Etsy ve Pinterest verilerine göre en çok satacak niş (niche) konuları bulmak.',
    backstory='Sektörde 10 yıllık deneyimli, trendleri önceden tahmin eden e-ticaret uzmanı.',
    verbose=True,
    memory=True
)

# Tasarımcı Ajan
tasarimci_ajan = Agent(
    role='POD Grafik Tasarımcısı',
    goal='Trend raporuna göre Midjourney ve DALL-E için görsel üretim komutları (prompt) yazmak.',
    backstory='Yapay zeka görsel komutları konusunda uzman, kreatif POD tasarımcısı.',
    verbose=True
)

# SEO ve Metin Yazarı Ajan
seo_ajani = Agent(
    role='Etsy SEO ve Listeleme Uzmanı',
    goal='Tasarım fikirlerine uygun başlık, 13 adet etiket (tags) ve açıklama yazmak.',
    backstory='Etsy algoritmasını çok iyi bilen, ürünleri aramalarda en üst sıraya çıkaran pazarlama uzmanı.',
    verbose=True
)

# 2. GÖREVLERİN (TASKS) TANIMLANMASI

gorev1 = Task(
    description='Bu hafta Etsy üzerinde hızlı satılabilecek, rekabeti düşük 3 özgün POD tişört/kupa niş konusu bul.',
    expected_output='3 adet detaylı trend niş konusu raporu.',
    agent=arge_ajani
)

gorev2 = Task(
    description='Bulunan 3 trend konu için Midjourney veya DALL-E 3 üzerinde harika sonuç verecek İngilizce görsel promptları hazırla.',
    expected_output='Her niş için 1 adet, toplamda 3 adet İngilizce görsel üretim promptu.',
    agent=tasarimci_ajan
)

gorev3 = Task(
    description='Üretilen tasarımlar için Etsy standartlarında 1 adet İngilizce başlık, 13 adet etiket ve SEO uyumlu ürün açıklaması yaz.',
    expected_output='3 ürün için de ayrı ayrı hazırlanmış başlık, etiket ve açıklama metinleri.',
    agent=seo_ajani
)

# 3. ŞİRKETİN (CREW) KURULMASI VE ÇALIŞTIRILMASI

etsy_sirketi = Crew(
    agents=[arge_ajani, tasarimci_ajan, seo_ajani],
    tasks=[gorev1, gorev2, gorev3],
    process=Process.sequential # Sırasıyla çalışırlar: ARGE -> Tasarım -> SEO
)

if __name__ == "__main__":
    print("🚀 Yapay Zeka Şirketi Çalışmaya Başlıyor...")
    sonuc = etsy_sirketi.kickoff()
    print("✅ İşlem Tamamlandı! İşte Sonuçlar:")
    print(sonuc)
