from budayaKB_model import BudayaItem, BudayaCollection
from flask import Flask, request, render_template


app = Flask(__name__)
app.secret_key ="tp4"

#inisialisasi objek budayaData
databasefilename = "" #nama file yg diimpor
budayaData = BudayaCollection()

#merender tampilan default(index.html)
@app.route('/')
def index():
	return render_template("index.html")

# Bagian ini adalah implementasi fitur Impor Budaya, yaitu:
# - merender tampilan saat menu Impor Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Import Data" diklik
# - menampilkan notifikasi bahwa data telah berhasil diimport 	

@app.route('/imporBudaya', methods=['GET', 'POST'])
#fungsi import data
def importData():                                                                               
	if request.method == "GET":
		return render_template("imporBudaya.html")

	elif request.method == "POST":
		f = request.files['file'] #meminta nama filenya
		global databasefilename
		databasefilename=f.filename #nama dari file yg diimpor
		budayaData.importFromCSV(f.filename) #mengimpor data dari csv ke bentuk dictionary yg valuenya objek budaya
		n_data = len(budayaData.koleksi) #panjang dictionary setelah diimpor
		return render_template("imporBudaya.html", result=n_data, fname=f.filename)

@app.route('/tambahBudaya', methods=['GET', 'POST'])
#fungsi menambah data yg belum ada di database
def tambahdata():
    if databasefilename == "":
        return render_template('tambahBudaya.html', error="blm")
    if request.method == "GET":
        return render_template("tambahBudaya.html")
    elif request.method == "POST":
        nambud = request.form["namabudaya"] #ngambil isi dari form
        tipebud = request.form["tipebudaya"]
        provbud = request.form["provbudaya"]
        urlbud = request.form["urlbudaya"]
        valid =budayaData.tambah(nambud, tipebud, provbud, urlbud) #jika budaya belum ada di database akan True
        if valid == 1:
            budayaData.exportToCSV(databasefilename)
        return render_template("tambahBudaya.html", valid=valid, nambud=nambud)

@app.route('/ubahBudaya', methods=['GET', 'POST']) #mau ubah budaya
def ubah():
    if databasefilename == "":
        return render_template('ubahBudaya.html', error="blm")
    if request.method == "GET":
        return render_template('ubahBudaya.html') 
    elif request.method == "POST":        
        nambud = request.form["namabudaya"] #ngambil isi dari form nama
        tipebud = request.form["tipebudaya"] #ngambil isi dari form tipe
        provbud = request.form["provbudaya"] #ngambil isi dari form provinsi
        urlbud = request.form["urlbudaya"] #ngambil isi dari form url
        valid = budayaData.ubah(nambud, tipebud, provbud, urlbud) #return True atau False
        if valid == 1:
            budayaData.exportToCSV(databasefilename) #ekspor utk ngubah data csv
        return render_template("ubahBudaya.html", valid=valid, nambud=nambud) 

@app.route('/hapusBudaya', methods=['GET', 'POST'])
def hapus():
    if databasefilename == "":
        return render_template('ubahBudaya.html', error="blm")
    if request.method == "GET":
        return render_template('hapusBUdaya.html') 
    elif request.method == "POST":        
        nambud = request.form["namabudaya"] #ambil isi dari nama yg mau diapus
        valid =budayaData.hapus(nambud) #jika budaya yg akan dihapus ada di database maka akan True
        if valid == 1:
            budayaData.exportToCSV(databasefilename)
        return render_template("hapusBUdaya.html", valid=valid, nambud=nambud)

@app.route('/cariBudaya', methods=['GET', 'POST'])
def caridata():
    if request.method == "GET":
        return render_template('cariBudaya.html')
    elif request.method == "POST": 
        warisan = request.form["bud"] #ambil isi dari nama budaya
        if request.form["perintah"] == "Nama Budaya":
            obj = request.form["perintah"] #ambil isi dari select
            lst = budayaData.cariByNama(warisan) #list yg isinya objek
            data = budayaData.koleksi.values() #ambil values yg berupa objek dari database keseluruhan
            return render_template("cariBudaya.html", warisan=warisan, obj=obj, pjg = len(lst), hasil=lst, data=data, panjang=len(data))
        elif request.form["perintah"] == "Tipe Budaya":
            obj = request.form["perintah"]
            lst = budayaData.cariByTipe(warisan)
            data = budayaData.koleksi.values()
            return render_template("cariBudaya.html", warisan=warisan, obj=obj, pjg = len(lst), hasil=lst, panjang=len(data))
        elif request.form["perintah"] == "Asal Provinsi Budaya":
            obj = request.form["perintah"]
            lst = budayaData.cariByProv(warisan)
            data = budayaData.koleksi.values()
            return render_template("cariBudaya.html", warisan=warisan, obj=obj, pjg = len(lst), hasil=lst, panjang=len(data))
            
        
@app.route('/statsBudaya', methods=['GET', 'POST'])
def stat():
    stat = budayaData.stat()
    if request.method == "GET":
        return render_template("statsBudaya.html")
    elif request.method == "POST":
        if request.form["perintah"] == "All":
            stat = budayaData.stat() #return panjang dari dict database umum
            select= request.form["perintah"] #return nama dari yg kita select di html
            return render_template('statsBudaya.html', select=select, banyak = stat)
        elif request.form["perintah"] == "Tipe Budaya":
            stat = budayaData.stat() 
            dict_ = budayaData.statByTipe() #dict yg keynya adalah tipe budaya dan valuesnya adalah frekuensi kemunculan si tipe
            select= request.form["perintah"]
            return render_template('statsBudaya.html', select=select, banyak = stat, data=dict_)
        elif request.form["perintah"] == "Asal Provinsi Budaya":
            stat = budayaData.stat()
            dict_ = budayaData.statByProv()
            select= request.form["perintah"]
            return render_template('statsBudaya.html', select=select, banyak = stat, data=dict_)



# run main app
if __name__ == "__main__":
	app.run(debug=True)


