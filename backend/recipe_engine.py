# backend/recipe_engine.py
# Kitchen Quest — Motor de Recetas v0.1

def crear_ingrediente(nombre, cantidad_g, calorias_100g, proteina_100g, carbs_100g, grasa_100g):
    """
    Crea un ingrediente con su información nutricional.
    Todo se calcula por 100g para estandarizar.
    """
    return {
        "nombre": nombre,
        "cantidad_g": cantidad_g,
        "calorias_100g": calorias_100g,
        "proteina_100g": proteina_100g,
        "carbs_100g": carbs_100g,
        "grasa_100g": grasa_100g
    }


def crear_receta(nombre, porciones, ingredientes=None):
    if not isinstance(porciones, (int, float)) or porciones <= 0:
        raise ValueError(f"Las porciones deben ser un número positivo. Recibido: {porciones}")
    
    return {
        "nombre": nombre,
        "porciones": porciones,
        "ingredientes": ingredientes or []
    }

def calcular_nutricion_ingrediente(ingrediente):
    """
    Calcula los macros reales según la cantidad usada en la receta.
    """
    factor = ingrediente["cantidad_g"] / 100

    return {
        "nombre": ingrediente["nombre"],
        "cantidad_g": ingrediente["cantidad_g"],
        "calorias": round(ingrediente["calorias_100g"] * factor, 1),
        "proteina_g": round(ingrediente["proteina_100g"] * factor, 1),
        "carbs_g": round(ingrediente["carbs_100g"] * factor, 1),
        "grasa_g": round(ingrediente["grasa_100g"] * factor, 1)
    }


def calcular_nutricion_receta(receta):
    """
    Suma los macros de todos los ingredientes y divide por porciones.
    Retorna totales de la receta completa Y por porción.
    """
    totales = {"calorias": 0, "proteina_g": 0, "carbs_g": 0, "grasa_g": 0}

    for ingrediente in receta["ingredientes"]:
        nutricion = calcular_nutricion_ingrediente(ingrediente)
        for key in totales:
            totales[key] += nutricion[key]

    # Redondear totales
    for key in totales:
        totales[key] = round(totales[key], 1)

    # Calcular por porción
    por_porcion = {
        key: round(totales[key] / receta["porciones"], 1)
        for key in totales
    }

    return {
        "receta": receta["nombre"],
        "porciones": receta["porciones"],
        "total": totales,
        "por_porcion": por_porcion
    }

def imprimir_reporte(nutricion):
    """Imprime un reporte legible de la información nutricional."""
    print(f"\n{'='*40}")
    print(f"  🍳 {nutricion['receta']}")
    print(f"  {nutricion['porciones']} porciones")
    print(f"{'='*40}")
    print(f"  TOTAL RECETA:")
    print(f"    Calorías:  {nutricion['total']['calorias']} kcal")
    print(f"    Proteína:  {nutricion['total']['proteina_g']} g")
    print(f"    Carbos:    {nutricion['total']['carbs_g']} g")
    print(f"    Grasa:     {nutricion['total']['grasa_g']} g")
    print(f"\n  POR PORCIÓN:")
    print(f"    Calorías:  {nutricion['por_porcion']['calorias']} kcal")
    print(f"    Proteína:  {nutricion['por_porcion']['proteina_g']} g")
    print(f"    Carbos:    {nutricion['por_porcion']['carbs_g']} g")
    print(f"    Grasa:     {nutricion['por_porcion']['grasa_g']} g")
    print(f"{'='*40}\n")


# ── PRUEBA ──────────────────────────────────────
if __name__ == "__main__":

    # Construye tu primera receta real
    avena = crear_ingrediente("Avena en hojuelas", 80, calorias_100g=389, proteina_100g=17, carbs_100g=66, grasa_100g=7)
    proteina = crear_ingrediente("Proteína en polvo", 30, calorias_100g=380, proteina_100g=75, carbs_100g=8, grasa_100g=5)
    leche = crear_ingrediente("Leche deslactosada", 200, calorias_100g=42, proteina_100g=3.4, carbs_100g=5, grasa_100g=1)
    banano = crear_ingrediente("Banano", 100, calorias_100g=89, proteina_100g=1.1, carbs_100g=23, grasa_100g=0.3)

    receta_avena = crear_receta("Avena Proteica Matutina", porciones=2)
    receta_avena["ingredientes"] = [avena, proteina, leche, banano]

    nutricion_avena = calcular_nutricion_receta(receta_avena)
    imprimir_reporte(nutricion_avena)

    # Construye otra receta
    arroz = crear_ingrediente("Arroz blanco", 150, calorias_100g=130, proteina_100g=2.7, carbs_100g=28, grasa_100g=0.3)
    pollo = crear_ingrediente("Pechuga de pollo", 200, calorias_100g=165, proteina_100g=22, carbs_100g=0, grasa_100g=1)
    aguacate = crear_ingrediente("Aguacate", 50, calorias_100g=160, proteina_100g=2, carbs_100g=9, grasa_100g=15)
    tomate = crear_ingrediente("Tomate crudo", 100, calorias_100g=18, proteina_100g=0.9, carbs_100g=3.9, grasa_100g=0.2)
    cebolla = crear_ingrediente("Cebolla cruda", 50, calorias_100g=40, proteina_100g=1.1, carbs_100g=9.3, grasa_100g=0.1)
    papa_frita = crear_ingrediente("Papas fritas", 100, calorias_100g=312, proteina_100g=3.4, carbs_100g=41, grasa_100g=15)

    receta_clasica = crear_receta("Comida Clásica", porciones=3)
    receta_clasica["ingredientes"] = [arroz, pollo, aguacate, tomate, cebolla, papa_frita]

    nutricion_clasica = calcular_nutricion_receta(receta_clasica)
    imprimir_reporte(nutricion_clasica)