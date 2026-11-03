# Guion del vídeo (español)

El reparto entre vosotros es solo una sugerencia. Decidlo con vuestras palabras siempre que podáis.
Total: 1274 words, about 8.8 minutes at 145 words per minute.


## Slide 1: Predicting myopia in medical students

**Ana** (about 16 s)

Hola, somos Ana y Tomás. En este proyecto intentamos predecir la miopía en estudiantes de tercero de Medicina. Con solo 132 estudiantes, la pregunta interesante no era solo qué modelo gana, sino cuánto podemos confiar en el resultado.

## Slide 2: The talk in three ideas

**Ana** (about 24 s)

Esta es la charla en tres ideas. Primera: los modelos complejos rara vez superan a una regresión logística simple con una sola medida, la longitud del ojo. Segunda: un cociente de la literatura médica dio un modelo nuevo que pasó nuestra prueba en todos los objetivos, aunque no probamos los modelos complejos con él. Y tercera: medimos lo optimistas que son nuestras puntuaciones, y parte de la mejora no supera esa comprobación.

## Slide 3: One dataset, four questions about myopia

**Ana** (about 26 s)

Los datos son de estudiantes de la Universidad de Navarra, y el enunciado pide cuatro predicciones. Si un estudiante tiene miopía. Si tiene miopía magna, es decir, más de seis dioptrías. Combo, que une ambas con una clase de control. Y DCombo, que además divide la miopía en dos tipos. Tenemos que generar etiquetas para 24 estudiantes de test cuyas respuestas no conocemos.

## Slide 4: Few students, few cases, and messy columns

**Ana** (about 41 s)

La principal dificultad es el tamaño. Hay 132 estudiantes de entrenamiento y solo 10 tienen miopía magna, así que responder siempre que no ya da un 92 por ciento de accuracy, y no sirve para nada. También encontramos problemas en los datos. El fototipo estaba mezclado con una columna vecina, así que falta el 45 por ciento. Y 8 estudiantes son miopía magna en Combo, pero no en la columna MM. Probamos a corregirlos y mantuvimos las etiquetas originales, porque el único resultado firme de la corrección fue una caída de la accuracy. Convertimos 49 columnas en 33 variables numéricas.

## Slide 5: With so little data, the method matters most

**Ana** (about 46 s)

Con tan pocos datos, lo que más importa es el método. Repetimos diez veces una validación cruzada estratificada de cinco bloques, porque una sola partición dependería de dónde caen unos pocos positivos. Todo lo que se aprende de los datos se queda dentro de los bloques de entrenamiento, y el ajuste usa validación cruzada anidada. Escribimos una prueba que un modelo debe superar para sustituir a otro más simple. Mira la balanced accuracy y el macro-F1, y también informamos de la accuracy. Una vía de esa prueba se añadió después de ver resultados de validación, y el informe lo dice. Los estudiantes de test solo se usan una vez, para predecir.

## Slide 6: Complex models rarely beat a one-feature baseline

**Tomás** (about 31 s)

Comparamos regresión logística, un SVM, un bosque aleatorio y XGBoost, que no vimos en clase. XGBoost construye árboles pequeños uno tras otro, y cada uno corrige los errores de los anteriores. El punto grande rojo anaranjado es la regresión logística solo con la longitud axial. En balanced accuracy es muy difícil de superar. Solo en Combo quedan claramente por encima el bosque aleatorio y XGBoost, empatados entre sí. Con 132 estudiantes, más complejidad sobre todo añadió ruido.

## Slide 7: Medicine gave us a better measurement

**Tomás** (about 36 s)

Así que miramos la medicina. Una persona es miope cuando el ojo es demasiado largo para la potencia de la córnea. El cociente entre la longitud axial y el radio corneal combina ambas cosas. Un estudio con 193 universitarios muestra que sube con la miopía, y en nuestros estudiantes también sube en cada escalón. Lo calculamos para cada estudiante, sin usar etiquetas. El enunciado no da las unidades de la queratometría, así que dedujimos que son dioptrías a partir de los datos, y lo decimos en el informe.

## Slide 8: With the ratio, a new model won on every target

**Tomás** (about 37 s)

Con el cociente, un modelo nuevo superó nuestra prueba en todos los targets. M y DCombo usan regresión logística con longitud axial y cociente. Combo usa un bosque aleatorio con el cociente añadido. Y MM usa regresión logística solo con el cociente, con un umbral ajustado. También probamos un modelo ordinal para DCombo, que respeta el orden de las clases. Pasó la prueba, pero quedó por debajo de la regresión logística con el cociente, así que no lo elegimos. Son puntuaciones de validación, y enseguida mostraremos que son optimistas.

## Slide 9: On MM, accuracy has a price: missed cases

**Tomás** (about 43 s)

MM muestra que la accuracy tiene un precio. Con el umbral por defecto, el modelo encuentra el 90 por ciento de los positivos, pero su accuracy queda por debajo de decir siempre que no. Con un umbral ajustado dentro de los datos de entrenamiento, la accuracy sube a 0,97, y encuentra el 79 por ciento. Volver a 0,5 encuentra aproximadamente un positivo más de cada diez, con unas doce falsas alarmas más. Mantuvimos el umbral ajustado, porque superó la segunda vía de nuestra prueba, y el test se evalúa con accuracy. En una clínica, la elección dependería de lo que cueste cada error.

## Slide 10: The cornea may explain the eight odd students

**Tomás** (about 34 s)

El cociente también aporta algo sobre los 8 estudiantes que se contradicen. Tienen los ojos tan largos como los del grupo MM, pero la córnea más plana, así que su cociente es más bajo. Una posible explicación es que la córnea compense en parte y los mantenga por debajo de seis dioptrías, mientras que Combo sigue a la longitud axial. Es solo una hipótesis sobre 8 estudiantes. No tenemos valores de refracción, y sus cocientes se solapan con los del grupo MM.

## Slide 11: We measured how optimistic our scores are

**Ana** (about 47 s)

Esta es la parte que más valoramos. Elegimos estos modelos con los mismos estudiantes que los puntúan, después de 42 pruebas de selección. Así que repetimos una aproximación de toda la selección dentro de los bloques. La mejora se mantiene en M, casi desaparece en MM para la balanced accuracy, y desaparece en DCombo. En Combo, al repetir la selección nunca salió el bosque que elegimos, y quedó por debajo de la longitud axial sola. También dimos información inútil a nuestra prueba. En Combo la sigue pasando aproximadamente una de cada tres veces, así que la elección de modelo ahí tiene poco respaldo. En M, MM y DCombo, la mejora real de la córnea supera a la de una córnea barajada. Así que la córnea parece aportar información real, pero las mejoras exactas son inciertas.

## Slide 12: Two features drive the models; errors stay close

**Ana** (about 37 s)

¿Qué usan los modelos? Casi solo la longitud axial y el cociente, incluso el bosque aleatorio, que tiene todas las variables disponibles. Eso describe a los modelos, no las causas de la miopía: la familia o el tiempo al aire libre podrían actuar a través de la longitud del ojo. ¿Y dónde fallan? Sobre todo entre clases vecinas. En DCombo, el 63 por ciento de las predicciones acierta, el 35 por ciento se queda a una clase, y el 2 por ciento más lejos. M1 es la clase más difícil.

## Slide 13: What we expect on the test set

**Ana** (about 39 s)

Esto es lo que esperamos en el test, antes de que se corrija. Con 24 estudiantes, solo el azar mueve el resultado cuatro o cinco alumnos, así que son rangos, no promesas. En M, Combo y DCombo, las dos estimaciones están por encima de la clase mayoritaria. En MM, van de quedar más o menos igual a superarla. Un riesgo: nuestro modelo dice miopía magna en 5 de los 24 estudiantes de test, frente al 8 por ciento en entrenamiento. Es compatible con el azar, y no lo cambiamos, porque sería elegir con el test. Además, 3 de los 24 estudiantes reciben etiquetas que se contradicen entre objetivos, por ejemplo sin miopía en M pero con miopía en Combo. Las dejamos como salieron.

## Slide 14: What we take away

**Tomás** (about 22 s)

Para terminar, tres ideas. En nuestras comparaciones, conocer el problema dio mejoras que la complejidad no dio, aunque no probamos los modelos complejos con el cociente, y la mejora que resiste nuestra comprobación anidada es clara sobre todo en M. Medir nuestras propias dudas forma parte del resultado, no es un extra. Y el límite está en parte en los datos: más estudiantes y una medida directa de la refracción probablemente ayudarían más que otro modelo. Gracias.

## Slide 15: Team and tools

**Tomás** (about 18 s)

Estas últimas diapositivas las pide el enunciado. Hicimos todas las partes juntos y tomamos las decisiones en conjunto, con un reparto de cincuenta-cincuenta. No usamos Keras ni PyTorch. Usamos scikit-learn y XGBoost, porque con 132 estudiantes las redes neuronales eran difíciles de justificar.

## Slide 16: How we used generative AI

**Tomás** (about 31 s)

Usamos IA generativa durante todo el trabajo, principalmente Claude Code. Generó buena parte del código y redactó el texto de los notebooks, respondió nuestras dudas conceptuales, propuso enfoques y reglas, encontró la literatura sobre el cociente, revisó el trabajo, construyó estas diapositivas y redactó el guion de este vídeo. Nosotros tomamos las decisiones, le propusimos ideas a la IA y llevamos un registro de su uso, que va incluido en la entrega. Gracias por vernos.
