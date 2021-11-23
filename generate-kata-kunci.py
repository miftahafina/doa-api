from doa_list import doa_list
from os import unlink
from shutil import copyfile
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

kata_kunci_list = []
stemmer         = StemmerFactory().create_stemmer()
temp_file_name  = "generated_doa_list_temp.py"
final_file_name = "generated_doa_list.py"
result = {
    "code"   : 200,
    "message": "Success",
    "data"   : []
}
id_doa = 0

for doa in doa_list:
    nama_doa_stem     = stemmer.stem(doa["nama"])
    kata_kunci_list   = nama_doa_stem.split(" ")
    doa["kata_kunci"] = kata_kunci_list
    
    id_doa += 1
    doa["id_doa"] = str(id_doa)

    file = open(temp_file_name, "w")
    file.write(f"generated_doa_list = {str(doa_list)}")
    file.close

    copyfile(temp_file_name, final_file_name)
    unlink(temp_file_name)

print(result)
