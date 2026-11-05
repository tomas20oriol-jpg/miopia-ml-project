# Guion del vídeo (español)

Sigue las 20 diapositivas de la presentación de Canva. El reparto entre ponentes es solo una sugerencia.
Total: 1212 words, about 9.3 minutes at 130 words per minute.

## Slide 1: Predicting myopia in medical students

**Ana** (about 16 s)

Hola, somos Ana y Tomás. Hemos intentado predecir la miopía en estudiantes de tercero de Medicina. Con solo 132 estudiantes, la pregunta no es solo qué modelo gana, sino cuánto podemos fiarnos del resultado.

## Slide 2: Index

**Ana** (about 16 s)

Empezamos por el problema y los datos, seguimos con cómo los preparamos y elegimos los modelos, cómo usamos la IA, los resultados y cuánto fiarnos de ellos, y terminamos con las conclusiones y el equipo.

## Slide 3: Four targets, 24 test students

**Ana** (about 32 s)

El enunciado pide cuatro predicciones por estudiante: si tiene miopía; si tiene miopía magna, es decir, más de seis dioptrías; Combo, que separa control, miopía y magna; y DCombo, que además divide la miopía en M1 y M2. La miopía magna es la que más importa, porque puede causar enfermedad de retina, y también es la clase más rara. Entregamos etiquetas para 24 estudiantes de test cuyas respuestas no tenemos.

## Slide 4: Data overview

**Tomás** (about 33 s)

Tenemos 132 estudiantes de entrenamiento con 49 columnas. Solo 10 están etiquetados con miopía magna, así que responder siempre que no ya da un 92 por ciento de accuracy y no encuentra a nadie. Por eso la accuracy sola no sirve para ordenar los modelos. Una variable destaca: la longitud axial, la longitud del ojo, que sube de 23,5 milímetros en los controles a 24,5 en miopía y 26,4 en miopía magna.

## Slide 5: Inconsistent labels

**Tomás** (about 34 s)

También encontramos 8 estudiantes con miopía magna en Combo pero no en la columna MM. Tres de sus cuatro objetivos dicen miopía magna, así que tratamos la columna MM como el error y la corregimos, lo que da 18 casos de magna. Sus ojos son tan largos como los del grupo magna, pero su córnea es más plana, así que podrían estar de verdad por debajo de seis dioptrías. Lo contamos como un riesgo.

## Slide 6: Cleaning and new features

**Tomás** (about 41 s)

Convertimos las 49 columnas en 32 variables numéricas. Quitamos 21: una vacía, doce que son combinación de otras, siete por criterio, y el fototipo, que estaba mezclado con una columna vecina y no servía para el 45 por ciento de los estudiantes. La imputación y el escalado se ajustan dentro de cada bloque de entrenamiento. Y añadimos una variable de la literatura médica: la longitud axial dividida por el radio de la córnea, porque la miopía aparece cuando el ojo es demasiado largo para la potencia de su córnea.

## Slide 7: Class imbalance

**Ana** (about 37 s)

Las clases están desequilibradas, así que hicimos cuatro cosas. Bloques estratificados, para que cada bloque conserve la clase magna. Pesos de clase equilibrados, para que las clases raras cuenten lo mismo al entrenar. Balanced accuracy y macro-F1 para elegir los modelos, siempre con la accuracy al lado. Y un umbral ajustado para MM, que probamos y no mejoró el 0,5 por defecto. La trampa es un modelo que siempre dice que no: parece preciso, pero no encuentra ningún caso de magna.

## Slide 8: Validation

**Ana** (about 36 s)

Con tan pocos datos, lo que más importa es la validación. Todo lo que aprende de los datos está en un pipeline que se reajusta en cada bloque de entrenamiento, así que nada se filtra. Repetimos diez veces una validación cruzada estratificada de cinco bloques y damos la dispersión, no un solo número. Los modelos ajustados usan validación cruzada anidada, con una búsqueda en rejilla interna. Y el test se usa una sola vez, solo para predecir.

## Slide 9: Candidate models

**Ana** (about 27 s)

Comparamos cuatro familias de modelos: regresión logística; un SVM con kernel RBF; un bosque aleatorio; y XGBoost, que no vimos en clase. Construye árboles pequeños uno detrás de otro, y cada uno corrige los errores de los anteriores. Además probamos dos ideas: el cociente axial/corneal y un modelo ordinal para DCombo, que respeta el orden de las clases.

## Slide 10: Decision rule

**Ana** (about 32 s)

Escribimos la regla de decisión antes de ejecutar los modelos. La referencia es la mejor línea base logística. Un candidato tiene que ser claramente mejor, es decir, su mejora media emparejada entre repeticiones tiene que superar una desviación típica, por una de dos vías, y tiene que pasar otra vez en bloques nuevos. La vía B se añadió después de ver resultados de validación, y el informe lo dice.

## Slide 11: How we used generative AI

**Tomás** (about 18 s)

Usamos IA generativa durante todo el trabajo, sobre todo Claude Code. Escribió buena parte del código y del texto de los notebooks, respondió dudas conceptuales, propuso enfoques y revisó la metodología y los gráficos. Las decisiones fueron nuestras.

## Slide 12: Baselines

**Ana** (about 25 s)

Primero, las líneas base. Responder siempre la clase mayoritaria no encuentra ningún caso de magna. La regresión logística solo con la longitud axial es fuerte: en balanced accuracy, las 32 variables no lo hacen mejor en ningún objetivo. Así que la mejor de las dos es el listón que todo modelo tiene que superar.

## Slide 13: Model comparison

**Ana** (about 28 s)

Frente a ese listón, los ensembles de árboles ganaron en dos objetivos: XGBoost en MM y el bosque aleatorio en Combo. El cociente ayudó en M, Combo y DCombo, pero no en MM, donde la longitud axial sola separa mejor las clases. A la derecha, el bosque de Combo se apoya casi solo en la longitud axial y el cociente.

## Slide 14: Final models

**Ana** (about 30 s)

Así que cada objetivo tiene su modelo. M: regresión logística con longitud axial y cociente, con balanced accuracy de 0,80. MM: XGBoost con las 32 variables y el umbral por defecto, con balanced accuracy de 0,90 y accuracy de 0,96, frente al 0,86 de decir siempre que no. Combo: el bosque aleatorio con el cociente, 0,77. DCombo: regresión logística con longitud axial y cociente, 0,65.

## Slide 15: Where the models fail

**Tomás** (about 30 s)

¿Dónde fallan los modelos? Sobre todo entre clases vecinas. En DCombo, el 63 por ciento de las predicciones aciertan, el 35 por ciento fallan por una clase y el 2 por ciento por más. M1 es la clase más difícil: a menudo se confunde con control. El modelo de MM pierde más o menos un caso de magna de cada seis, con muy pocas falsas alarmas.

## Slide 16: How optimistic are the scores

**Tomás** (about 44 s)

Elegimos estos modelos con los mismos estudiantes que los puntúan, después de 44 pruebas de selección, así que las puntuaciones los favorecen. Repetimos toda la selección dentro de los bloques. La mejora sobre la longitud axial se mantiene en M y en MM, donde XGBoost se elige en todos los bloques. Desaparece en DCombo, y en Combo la selección repetida queda por debajo de la longitud axial. Con información inútil, nuestra prueba todavía pasa una de cada tres veces en Combo, así que esa elección es débil. Las puntuaciones de validación cruzada son un techo.

## Slide 17: Expected test accuracy

**Tomás** (about 34 s)

Esto es lo que esperamos en el test. Con 24 estudiantes, cada uno vale 0,04 de accuracy, y solo el azar mueve el resultado cuatro o cinco estudiantes. Esperamos los cuatro objetivos por encima de la clase mayoritaria, MM con claridad. Un riesgo: nuestro modelo dice miopía magna para 5 de los 24 estudiantes de test, más que en entrenamiento, pero compatible con el azar. No cambiamos ninguna etiqueta después de ver el test.

## Slide 18: Conclusions

**Ana** (about 33 s)

Para terminar. Lo simple primero: la longitud axial y una regresión logística igualaron a modelos complejos en M y DCombo. El conocimiento del dominio ayudó: el cociente dio mejoras, sobre todo en M. Y medir nuestra duda es parte del resultado. Los límites están en los datos: 132 estudiantes, 18 casos de magna y ningún valor de refracción. Más estudiantes y una medida directa de la refracción ayudarían más que otro modelo.

## Slide 19: Team and tools

**Tomás** (about 12 s)

Tomás y Ana hicimos todas las partes juntos, y el trabajo se repartió al cincuenta por ciento. Nuestros modelos están hechos con scikit-learn y XGBoost.

## Slide 20: Thank you

**Ana** (about 2 s)

Gracias por vuestra atención.
