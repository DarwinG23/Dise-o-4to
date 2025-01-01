class Cedula:
    def validar_cedula(cedula):
        if len(cedula) != 10 or not cedula.isdigit():
            return False

        provincia = int(cedula[:2])
        if provincia < 1 or (provincia > 24 and provincia != 30):
            return False

        tercer_digito = int(cedula[2])
        if tercer_digito < 0 or tercer_digito > 6:
            return False

        coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        suma = 0

        for i in range(9):
            digito = int(cedula[i]) * coeficientes[i]
            if digito > 9:
                digito -= 9
            suma += digito

        modulo = suma % 10
        digito_verificador = 10 - modulo if modulo != 0 else 0

        return digito_verificador == int(cedula[9])

    # Ejemplo de uso
    cedula = "0102030405"
    if validar_cedula(cedula):
        print("Cédula válida")
    else:
        print("Cédula inválida")