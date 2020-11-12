import csv,sys

# #este no lo muevas, es solo el id desde el cual inicia django a guardar
# #internamente django busca el id mas grande e inicia a escribir desde ese
init_seed=11000

# #users
from django.contrib.auth.hashers import PBKDF2PasswordHasher
hasher = PBKDF2PasswordHasher()

fields=["id","password","last_login","is_superuser","groups","user_permissions","username","first_name","last_name","email", "is_staff", "is_active","date_joined"]
# print(sys.argv[1])
try:
    file_read=open(sys.argv[1],"r")
except Exception as e:
    raise e
    print("error leyendo el archivo de datos:"+sys.argv[1])
try:
    file_write=open(sys.argv[2],"w")
    csv_reader = csv.reader(file_read, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            writer=csv.DictWriter(file_write,fieldnames=fields)
            writer.writeheader()
            line_count += 1
        else:
            # print("asd:"+row[0]+"-"+row[4])
            # mail=>pass
            password = hasher.encode(password=row[1], salt='salt', iterations=150000)
            writer.writerow({"id":init_seed+line_count,"password":password, "last_login":"","is_superuser":0,"groups":"","user_permissions":"","username":row[3],"first_name":row[2],"last_name":"","email":row[1], "is_staff":0, "is_active":1,"date_joined":""})
            line_count += 1
    # print(line_count)
    file_read.close()
    file_write.close()


except Exception as e:
    raise e
    print("error en el archivo de escritura:"+sys.argv[2])
    


