import pandas as pd
import os
from extract import extract_text_from_pdf, segment_text, extract_data_with_regex, enhanced_segmenter
from bert_qa import BERTQA

def main():
    try:
        # 1. Extraer texto del PDF
        pdf_text = extract_text_from_pdf("../data/EjemploLicitacion.pdf")
        
        if not pdf_text:
            print("❌ Error: No se pudo extraer texto del PDF.")
            return

        # 2. Segmentar el texto en secciones clave
        sections = enhanced_segmenter(pdf_text)
        print("\n🔍 Secciones detectadas:", list(sections.keys()))

        # 3. Extracción estructurada con regex
        regex_data = extract_data_with_regex(pdf_text)
        print("\n📊 Datos extraídos con regex:", regex_data)

        # 4. Validar campos críticos
        required_fields = ["expediente", "valor_estimado", "cpv"]
        missing_fields = [field for field in required_fields if not regex_data.get(field)]
        if missing_fields:
            print(f"\n⚠️  Advertencia: Campos faltantes - {', '.join(missing_fields)}")

        # 5. Cargar modelo BERT afinado
        try:
            print("\n🤖 Cargando modelo BERT afinado...")
            bert_qa = BERTQA(use_finetuned=True)
        except Exception as e:
            print(f"\n❌ Error cargando modelo afinado: {e}")
            print("🔁 Usando modelo BERT base como respaldo...")
            bert_qa = BERTQA(use_finetuned=False)

        # 6. Preguntas clave con contexto optimizado
        preguntas = {
            "valor_estimado_bert": {
                "pregunta": "¿Cuál es el valor estimado exacto del contrato en euros?",
                "contexto": sections.get("objeto_contrato", pdf_text)
            },
            "plazo_ejecucion_bert": {
                "pregunta": "¿Cuál es el plazo total de ejecución en meses?",
                "contexto": sections.get("condiciones", pdf_text)
            },
            "clasificacion_cpv": {
                "pregunta": "¿Cuál es el código CPV completo de la clasificación?",
                "contexto": sections.get("proceso", pdf_text)
            }
        }


        # 7. Procesar preguntas con BERT
        bert_responses = {}
        print("\n🔎 Analizando con BERT:")
        for key, config in preguntas.items():
            respuesta = bert_qa.answer(
                context=config["contexto"],
                question=config["pregunta"]
            )
            bert_responses[key] = {
                "respuesta": respuesta.get("answer", "No encontrado"),
                "confianza": f"{respuesta.get('score', 0):.1%}" if 'score' in respuesta else "N/A"
            }
            print(f"• {config['pregunta']}: {bert_responses[key]['respuesta']} ({bert_responses[key]['confianza']})")

        # 8. Validación cruzada y consolidación de datos
        final_data = {
            **regex_data,
            "valor_bert": bert_responses["valor_estimado_bert"]["respuesta"],
            "plazo_bert": bert_responses["plazo_ejecucion_bert"]["respuesta"],
            "cpv_bert": bert_responses["clasificacion_cpv"]["respuesta"]
        }

        # 9. Generar informe de consistencia
        print("\n📝 Informe de consistencia:")
        consistency_report = []
        for field in ["valor_estimado", "cpv"]:
            bert_key = f"{field}_bert"
            print(bert_key)
            if bert_key not in final_data:
                print(f"❌ Error crítico: '{bert_key}' no encontrado en final_data")
                print("🔧 Revise los logs y valide el formato del PDF")
                continue  # Evita que el programa falle y sigue con el siguiente campo
            
            regex_val = str(regex_data.get(field, "")).lower().replace(" ", "")
            bert_val = str(final_data[bert_key]).lower().replace(" ", "")
            
            status = "✅ Concordancia" if regex_val == bert_val else "⚠️ Discrepancia"
            consistency_report.append(f"{status} en {field}:")
            consistency_report.append(f"   - Regex: {regex_data.get(field, 'N/A')}")
            consistency_report.append(f"   - BERT: {final_data[bert_key]}")

        print("\n".join(consistency_report))

        # 10. Guardar resultados
        os.makedirs("output", exist_ok=True)
        df = pd.DataFrame([final_data])
        csv_path = "output/licitacion_analizada.csv"
        df.to_csv(csv_path, index=False)
        print(f"\n💾 Resultados guardados en: {csv_path}")
        print(df.head())

    except Exception as e:
        print(f"\n❌ Error crítico: {str(e)}")
        print("🔧 Revise los logs y valide el formato del PDF")

if __name__ == "__main__":
    main()