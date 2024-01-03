# Documentation
# https://docs.databricks.com/pt/sql/language-manual/functions/aes_encrypt.html

from pyspark.sql.functions import *
from pyspark.sql.types import *

# Create dataframe pyspark
data = [(
    "João",25,"Masculino",
), (
    "Maria",20,"Feminino",
), (
    "Marceline",45,"Feminino",
), (
    "Pedro",30,"Masculino",
)]

df = spark.createDataFrame(data, schema=["nome", "idade", "sexo"]).show()

# Create key in based 32 bytes
# The algorithm depends on the length of the key:
# 16: AES-128
# 24: AES-192
# 32: AES-256

encryption_key = 'your key in based 32'

# Created two columns with encryption and decryption 
jujuba = df.withColumn(
    'teste_encryption', expr(f"base64(aes_encrypt(nome, '{encryption_key}', 'ECB'))")
).withColumn(
    'teste_descryption', expr(f"aes_decrypt(unbase64(teste_encryption), '{encryption_key}', 'ECB')").cast(StringType())
).show()