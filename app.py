import streamlit as st
import pandas as pd

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

if 'users_db' not in st.session_state:
    # Key: username, Value: {'password': pass, 'name': full_name}
    st.session_state['users_db'] = {'admin': {'password': 'admin', 'name': 'Administrator'}}

if 'data_mahasiswa' not in st.session_state:
    st.session_state['data_mahasiswa'] = []

def tentukan_nilai(skor):
    """
    Fungsi ini adalah Rule-Based System sederhana yang mengonversi 
    skor angka menjadi nilai huruf dan keterangan lulus/tidak.
    """
    if skor >= 85:
        return "A", "Sangat Baik (Lulus)"
    elif skor >= 70:
        return "B", "Baik (Lulus)"
    elif skor >= 60:
        return "C", "Cukup (Lulus)"
    elif skor >= 50:
        return "D", "Kurang (Tidak Lulus)"
    else:
        return "E", "Sangat Kurang (Tidak Lulus)"

def auth_page():
    st.title("🔐 Akses Sistem Penilaian")
    
    # Gunakan tab untuk memisahkan Login dan Registrasi
    tab_login, tab_daftar = st.tabs(["Masuk", "Daftar Akun Baru"])
    
    with tab_login:
        with st.form("login_form"):
            user = st.text_input("Username")
            pw = st.text_input("Password", type="password")
            btn_login = st.form_submit_button("Masuk")
            
            if btn_login:
                if user in st.session_state['users_db'] and st.session_state['users_db'][user]['password'] == pw:
                    st.session_state['logged_in'] = True
                    st.session_state['current_user'] = st.session_state['users_db'][user]['name']
                    st.success(f"Selamat datang, {st.session_state['current_user']}!")
                    st.rerun()
                else:
                    st.error("Username atau password salah!")

    with tab_daftar:
        with st.form("reg_form"):
            new_user = st.text_input("Username Baru")
            new_name = st.text_input("Nama Lengkap")
            new_pw = st.text_input("Password", type="password")
            btn_reg = st.form_submit_button("Daftar Sekarang")
            
            if btn_reg:
                if new_user and new_name and new_pw:
                    if new_user in st.session_state['users_db']:
                        st.warning("Username sudah digunakan, pilih yang lain.")
                    else:
                        st.session_state['users_db'][new_user] = {'password': new_pw, 'name': new_name}
                        st.success("Akun berhasil dibuat! Silakan pindah ke tab 'Masuk'.")
                else:
                    st.error("Mohon isi semua data.")

def main_app():
    st.title("🎓 Sistem Penilaian Mahasiswa")
    st.caption("Aplikasi Rule-Based System menggunakan Streamlit")
    
    st.sidebar.markdown(f"### 👋 Halo,")
    st.sidebar.title(f"{st.session_state['current_user']}")
    st.sidebar.divider()
    
    if st.sidebar.button("Logout", type="primary"):
        st.session_state['logged_in'] = False
        st.session_state['current_user'] = None
        st.rerun()

    # Membuat Tab untuk fitur CRUD agar antarmuka lebih rapi
    tab_create, tab_read, tab_update, tab_delete = st.tabs([
        "➕ Tambah Data (Create)", 
        "📋 Lihat Data (Read)", 
        "✏️ Ubah Data (Update)", 
        "🗑️ Hapus Data (Delete)"
    ])

    # --- C: CREATE (Tambah Data) ---
    with tab_create:
        st.subheader("Input Nilai Mahasiswa Baru")
        with st.form("form_tambah"):
            nama = st.text_input("Nama Mahasiswa")
            skor = st.number_input("Skor Nilai (0-100)", min_value=0, max_value=100, step=1)
            submit_tambah = st.form_submit_button("Simpan Data")
            
            if submit_tambah:
                if nama:
                    # Terapkan Rule-Based System di sini
                    huruf, keterangan = tentukan_nilai(skor)
                    
                    # Simpan ke session state
                    st.session_state['data_mahasiswa'].append({
                        "Nama": nama,
                        "Skor": skor,
                        "Nilai Huruf": huruf,
                        "Keterangan": keterangan
                    })
                    st.success(f"Data atas nama {nama} berhasil ditambahkan!")
                else:
                    st.warning("Nama mahasiswa tidak boleh kosong!")

    # --- R: READ (Lihat Data) ---
    with tab_read:
        st.subheader("Rekapitulasi Nilai Mahasiswa")
        if st.session_state['data_mahasiswa']:
            # Konversi list of dictionary ke Pandas DataFrame agar tampilan tabel bagus
            df = pd.DataFrame(st.session_state['data_mahasiswa'])
            # Ubah index dimulai dari 1 (opsional agar lebih rapi)
            df.index = df.index + 1
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Belum ada data mahasiswa yang diinput. Silakan tambah data di tab 'Tambah Data'.")

    # --- U: UPDATE (Ubah Data) ---
    with tab_update:
        st.subheader("Ubah Skor Mahasiswa")
        if st.session_state['data_mahasiswa']:
            # Ambil daftar nama untuk dipilih
            daftar_nama = [data["Nama"] for data in st.session_state['data_mahasiswa']]
            pilihan_nama = st.selectbox("Pilih Mahasiswa", daftar_nama, key="update_select")
            
            # Cari indeks dari mahasiswa
            indeks_dipilih = daftar_nama.index(pilihan_nama)
            data_saat_ini = st.session_state['data_mahasiswa'][indeks_dipilih]
            
            with st.form("form_ubah"):
                st.write(f"Mengubah data untuk: **{pilihan_nama}**")
                skor_baru = st.number_input("Skor Baru", min_value=0, max_value=100, step=1, value=data_saat_ini["Skor"])
                submit_ubah = st.form_submit_button("Update Data")
                
                if submit_ubah:
                    # Jalankan ulang logic
                    huruf_baru, ket_baru = tentukan_nilai(skor_baru)
                    
                    # Update data
                    st.session_state['data_mahasiswa'][indeks_dipilih]["Skor"] = skor_baru
                    st.session_state['data_mahasiswa'][indeks_dipilih]["Nilai Huruf"] = huruf_baru
                    st.session_state['data_mahasiswa'][indeks_dipilih]["Keterangan"] = ket_baru
                    st.success("Data berhasil diperbarui!")
                    st.rerun() # Refresh
        else:
            st.info("Belum ada data untuk diubah.")

    # --- D: DELETE (Hapus Data) ---
    with tab_delete:
        st.subheader("Hapus Data Mahasiswa")
        if st.session_state['data_mahasiswa']:
            daftar_nama_hapus = [data["Nama"] for data in st.session_state['data_mahasiswa']]
            pilihan_hapus = st.selectbox("Pilih Mahasiswa yang akan dihapus", daftar_nama_hapus, key="delete_select")
            
            if st.button("Hapus Data!", type="primary"):
                indeks_hapus = daftar_nama_hapus.index(pilihan_hapus)
                st.session_state['data_mahasiswa'].pop(indeks_hapus)
                st.success(f"Data {pilihan_hapus} berhasil dihapus dari sistem.")
                st.rerun()
        else:
            st.info("Belum ada data untuk dihapus.")

# Cek apakah user sudah login atau belum
if not st.session_state['logged_in']:
    auth_page()
else:
    main_app()