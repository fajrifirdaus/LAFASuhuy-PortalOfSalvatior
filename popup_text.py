from messages import *

def show_opening_popup(display_surface):
    
    opening_text = [
        "Dimasa depan kondisi bumi semakin keritis, seorang astronot ditugaskan mencari sumber daya baru",
        "Pada saat tiba di Blue Pinwheel Galaxy, terjadi badai matahari yang merusak komponen roket. ",
        "memaksa pendaratan darurat di planet terdekat",
        "sang astronot tiba di planet sagaras, menemukan artefak kuno milik klan bintang",
        "dalam artefak tersebut menyebutkan sumber daya tak terbatas di planet tersebut",
        "bantu sang astronot menemukan artefaknya..."
    ]

    show_text = Message(opening_text, display_surface)
    # , -850, -150)
    show_text.run()

def show_crystal1(display_surface):
    text_crystal1 = [
        "Selamat kamu menemukan Pyronite Core",
        "Kumpulkan Pustaka klan bintang yang lain",
        "Petualanganmu yang penuh keberanian dan ketekunan telah membuahkan hasil."
    ]
    # show_text = Message(text_crystal1, -3000, -150)
    show_text = Message(text_crystal1, display_surface)
    show_text.run()

def show_crystal2(display_surface):
    text_crystal2 = [
        "Verdant Shard telah ditemukan",
        "Hati Hati perjalanan di planet ini semakin berbahaya !!"
    ]
    show_text = Message(text_crystal2, display_surface)
    show_text.run()

def show_crystal3(display_surface):
    text_crystal3 = [
        "Void Fragment sebagai pusaka terakhir telah anda temukan",
        "satukan seluruh crystal yang anda kumpulkan",
    ]
    show_text = Message(text_crystal3, display_surface)
    show_text.run()

def show_crystal_complete(display_surface):
    text_crystal_complete = [
        "Selamat crystal anda telah lengkap",
        "Gunakanlah Portal klan Bintang dengan bijak"
    ]
    show_text = Message(text_crystal_complete, display_surface)
    show_text.run()

def show_crystal_not_complete(display_surface):
    text_crystal_not_complete = [
        "Lengkapkan crystal untuk membuka portal klan bintang"
    ]
    show_text = Message(text_crystal_not_complete, display_surface)
    show_text.run()

def show_portal(display_surface):
    text_portal = [
        "Petualangan anda telah usai",
        "kamu telah menyelesaikan misi dengan baik, selamattt!!!"
    ]
    show_text = Message(text_portal, display_surface)
    show_text.run()

def show_crystal4(display_surface):
    text_crystal4 = [
        "Sayangnya, crystal yang kamu temukan tidak dapat menyembuhkan penyakit keluargamu...",
        "Meski telah berjuang keras,",
        "usaha ini belum membuahkan hasil. Jangan menyerah, masih ada harapan di masa depan."
    ]
    show_text = Message(text_crystal4, display_surface)
    show_text.run()

def show_death(display_surface):
    text_death = [
        "Dalam pencarian pustaka klan bintang",
        "sang astronot mengalami kematian tragis",
        "Harapan penyelamatan bumi di masa depan pupus bersama dengan kepergian sang astronot"
    ]
    show_text = Message(text_death, display_surface)
    show_text.run()