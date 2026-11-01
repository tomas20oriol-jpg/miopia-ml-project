# Video script (English)

The split between speakers is only a suggestion. Say it in your own words where you can.
Total: 1222 words, about 9.4 minutes at 130 words per minute.


## Slide 1: Predicting myopia in medical students

**Ana** (about 18 s)

Hello, we are Ana and Tomás. In this project we tried to predict myopia in third-year medical students. With only 132 students, the interesting question was not only which model wins, but how much we can trust the result.

## Slide 2: The talk in three ideas

**Ana** (about 26 s)

Here is the talk in three ideas. First, complex models rarely beat a simple logistic regression on one measurement, the length of the eye. Second, a ratio from the medical literature helped more than adding complexity. And third, we measured how optimistic our own scores are, and part of the gain does not survive that check.

## Slide 3: One dataset, four questions about myopia

**Ana** (about 30 s)

The data come from students at the University of Navarra, and the brief asks for four predictions. Whether a student has myopia. Whether they have myopia magna, which is more than six dioptres. Combo, which joins both with a control class. And DCombo, which also splits myopia into two types. We have to produce labels for 24 test students whose answers we do not have.

## Slide 4: Few students, few cases, and messy columns

**Ana** (about 45 s)

The main difficulty is the size. There are 132 training students, and only 10 have myopia magna, so always answering no already gets 92 percent accuracy, and is useless. We also found problems in the data. Phototype was mixed up with a neighbouring column, so 45 percent of it is missing. And 8 students are myopia magna in Combo, but not in the MM column. We tried correcting them, and kept the labels as provided, because the only firm result of the correction was a drop in accuracy. We turned 49 raw columns into 33 numeric features.

## Slide 5: With so little data, the method matters most

**Ana** (about 43 s)

With so little data, the method matters most. We repeat stratified five-fold cross-validation ten times, because a single split would depend on where a few positives land. Everything learned from data stays inside the training folds, and tuning uses nested cross-validation. We wrote down a test that a model must pass to replace a simpler one. It looks at balanced accuracy and macro-F1, and we report accuracy too. One route of that test was added after seeing validation results, and the report says so. The test students are used only once, to predict.

## Slide 6: Complex models rarely beat a one-feature baseline

**Tomás** (about 34 s)

We compared logistic regression, an SVM, a random forest and XGBoost, which we did not see in class. XGBoost builds small trees one after another, each one correcting the errors of the previous ones. In orange is logistic regression on axial length alone. On balanced accuracy it is very hard to beat. Only the random forest on Combo is clearly higher, and XGBoost never comes first. With 132 students, more complexity mostly added noise.

## Slide 7: Medicine gave us a better measurement

**Tomás** (about 39 s)

So we looked at the medicine. A person is myopic when the eye is too long for the power of the cornea. The ratio of axial length to corneal radius combines both. A study of 193 university students reports it rising with myopia, and in our students it rises at each step too. We compute it for each student, without using labels. The brief does not give the units of keratometry, so we deduced dioptres from the data, and we say so in the report.

## Slide 8: With the ratio, a new model won on every target

**Tomás** (about 43 s)

With the ratio, a new model passed our test on every target. M and DCombo use logistic regression on axial length plus the ratio. Combo uses a random forest with the ratio added. And MM uses logistic regression on the ratio alone, with a tuned threshold. We also tried an ordinal model for DCombo, which respects the order of the classes. It passed the test, but scored below logistic regression with the ratio, so we did not choose it. These are validation scores, and in a moment we will show that they are optimistic.

## Slide 9: On MM, accuracy has a price: missed cases

**Tomás** (about 45 s)

MM shows that accuracy has a price. At the default threshold, the model finds 90 percent of the positives, but its accuracy is below always saying no. With a threshold tuned inside the training data, accuracy rises to 0.97, and the model finds 79 percent. Going back to 0.5 finds about one more of the ten positives, with about twelve more false alarms. We kept the tuned threshold, because it passed the second route of our test, and the test set is graded on accuracy. In a clinic, the choice would depend on what each error costs.

## Slide 10: The cornea may explain the eight odd students

**Tomás** (about 34 s)

The ratio also sheds light on the 8 students who contradict themselves. Their eyes are as long as those in the MM group, but their corneas are flatter, so their ratio is lower. One possible explanation is that the cornea partly compensates, keeping them under six dioptres, while Combo follows axial length. This is only a hypothesis about 8 students. We have no refraction values, and their ratios overlap with the MM group.

## Slide 11: We measured how optimistic our scores are

**Ana** (about 50 s)

This is the part we value most. We chose these models with the same students who score them, after 42 selection tests. So we repeated an approximation of the whole selection inside the folds. The gain stays on M, nearly disappears on MM for balanced accuracy, and disappears on DCombo. We also gave our test useless information. On Combo it still passes about one time in three, so the choice of model there is weakly supported. On M, MM and DCombo, the real gain from the cornea is above what a shuffled cornea gives. So the cornea seems to carry real information, but the exact gains are uncertain.

## Slide 12: Two features drive the models; errors stay close

**Ana** (about 35 s)

What do the models use? Almost only axial length and the ratio, even the random forest, which has all the features available. That describes the models, not the causes of myopia: family or time outdoors could act through the length of the eye. And where do they fail? Mostly between neighbouring classes. In DCombo, 63 percent of predictions are right, 35 percent are one class away, and 2 percent further. M1 is the hardest class.

## Slide 13: What we expect on the test set

**Ana** (about 44 s)

This is what we expect on the test set, before it is graded. With 24 students, sampling alone moves a score by four or five students, so these are ranges and not promises. On M, Combo and DCombo, both estimates are above the majority class. On MM, they go from about level with it to above it. One risk: our model says myopia magna for 5 of the 24 test students, against 8 percent in training. That is compatible with chance, and we did not change it, because that would be choosing with the test set.

## Slide 14: What we take away

**Tomás** (about 24 s)

To conclude, three ideas. In our comparisons, knowing the problem helped more than adding complexity. Measuring our own doubt is part of the result, and not an extra. And the limit is partly the data: more students and a direct measure of refraction would likely help more than another model. Thank you.

## Slide 15: Team and tools

**Tomás** (about 20 s)

These last slides are required by the brief. We did all the parts together and took the decisions jointly, with a fifty-fifty split. We used neither Keras nor PyTorch. We used scikit-learn and XGBoost, because with 132 students neural networks were hard to justify.

## Slide 16: How we used generative AI

**Tomás** (about 34 s)

We used generative AI throughout the work, mainly Claude Code. It generated much of the code and drafted the notebook text, answered our conceptual questions, proposed approaches and rules, found the literature on the ratio, reviewed the work, built these slides and drafted the script for this video. We took the decisions, proposed ideas to the AI, and kept a log of its use, which is included in the delivery. Thank you for watching.
