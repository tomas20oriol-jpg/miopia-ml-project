# Speaker notes

## Slide 1: Predicting myopia in medical students

Hello. We are Ana and Tomás. This is our final project for the Machine Learning course. We predict myopia in third-year medical students, and we will show how we chose our models, and how much we trust the results. About 20 seconds.

## Slide 2: One dataset, four questions about myopia

The data come from third-year medical students at the University of Navarra. The brief asks for four predictions on 24 students with no labels. M is myopia, MM is myopia magna, above 6 dioptres. Combo joins them, and DCombo splits myopia into two types. Different models are allowed per task. About 40 seconds.

## Slide 3: Few students, few cases, and messy columns

We have only 132 training students, and only 10 with myopia magna. So a model that always says no gets 92 percent accuracy and is useless. Exploring the data we found problems: phototype was mixed up with another column, so 45 percent of it is missing. And 8 students are myopia magna in Combo but not in the MM column. We turned 49 raw columns into 33 numeric features, and justified each one. About 50 seconds.

## Slide 4: With so little data, the method matters most

One validation split would depend on which of the 10 positives land in it. So we repeat stratified 5-fold cross-validation 10 times, which leaves exactly 2 positives per fold in MM. Hyperparameters are tuned in nested cross-validation, and all preprocessing is fitted inside each fold. We do not select on accuracy alone, but we report it because the test is graded on it. Before choosing any model we wrote down a test it must pass. One route of that test was added after seeing validation results, never the test set, and the notebook says so. And the test set is used only once, to predict. About 60 seconds.

## Slide 5: Complex models rarely beat a one-feature baseline

We compared logistic regression, an SVM, a random forest and XGBoost, which we did not see in class. XGBoost builds small trees one after another, each correcting the errors of the previous ones. In orange is logistic regression on axial length alone. On balanced accuracy it is very hard to beat: only the random forest on Combo is clearly higher. XGBoost never came first. With 132 students, adding features and complexity brought mostly noise. About 50 seconds.

## Slide 6: Medicine gave us what complexity did not

So we looked at the medicine. A person is myopic when the eye is too long for the power of the cornea. The ratio of axial length to corneal radius combines both. The literature, including a study of 193 university students, shows it rising with myopia, and in our students it rises at each step too. We computed it for each student without using labels. The units of keratometry are not stated, so we deduced dioptres from the data. About 50 seconds.

## Slide 7: With the ratio, a new model won on every target

Here are the final models, compared with the baseline of axial length alone. M and DCombo use logistic regression on axial length plus the ratio. Combo uses a random forest with the ratio added. MM uses logistic regression on the ratio alone, with a tuned threshold. We also tried an ordinal model for DCombo, not seen in class either, and it did not beat this. These are validation scores, and they are optimistic, as we will show. About 50 seconds.

## Slide 8: On MM, accuracy has a price: missed cases

The MM model is a good example of a decision. With a threshold of 0.5 it finds 90 percent of positives, but its accuracy is below always saying no. Tuning the threshold inside the training data raises accuracy to 0.97, and it misses more cases. It passed the second route of our test, the one added after seeing validation results, and the test set is graded on accuracy. In a clinic the balance could differ: a threshold of 0.5 finds about one more of the 10 positives, with about 12 more false alarms, so it depends on the cost of each error. The choice is not fully firm: when we repeated the inner split, the criterion that passed changed. About 50 seconds.

## Slide 9: The cornea may explain the eight odd students

Remember the 8 students who contradict themselves. Their eyes are as long as true MM cases, but their corneas are flatter, so their ratio is lower. One possible explanation is that the cornea partly compensates, so they stay under 6 dioptres, while Combo follows axial length. This is a hypothesis about 8 students: we have no refraction values, and their ratios overlap with the MM group. It is the kind of question we would take to an ophthalmologist. About 40 seconds.

## Slide 10: We measured how optimistic our scores are

This is the slide we are most proud of. We chose these models using the same students who score them, after 42 selection tests. So we repeated an approximation of the whole selection inside the folds. The gain stays on M, nearly disappears on MM for balanced accuracy, and disappears on DCombo. We also fed our test useless information. On Combo it still passes about one time in three, so the choice of model there is weakly supported. On M and DCombo the real gain from the cornea is above chance. About 60 seconds.

## Slide 11: Most errors fall between neighbouring classes

What do the models use? Almost only axial length and the ratio, even the random forest, which has access to all the features. This does not mean that family or time outdoors have no effect: they may act through the length of the eye. Most errors are between neighbouring classes. In DCombo, 63 percent are right, 35 percent are one class away, and only 2 percent further. M1 is the hardest class, since without a direct measure of dioptres the line between mild myopia and none is blurred. About 50 seconds.

## Slide 12: What we expect on the test set

Before the labels are graded, this is what we expect. With 24 students, one student is worth about 0.04 of accuracy, and sampling alone moves a score by 4 to 5 students, so these are ranges and not promises. Both estimates are above the majority class on M, Combo and DCombo. MM goes from about level with the majority class to above it. And one risk: our model says myopia magna for 5 of the 24 test students, more than the 8 percent in training. That difference is compatible with chance, and we could not tell whether those are severe cases or false alarms. We did not change them, because that would be choosing with the test set. About 50 seconds.

## Slide 13: What we take away

To conclude. First, with this little data, knowing the problem beat adding complexity. Second, the process matters as much as the score, and that includes admitting what we cannot be sure of. Third, the limit is partly the data: more students and a direct measure of refraction would help more than any model. Thank you. About 40 seconds.

## Slide 14: Team and tools

These last slides are required by the brief. We did the work together, and took the decisions together, with a 50/50 split. We did not use Keras or PyTorch: with 132 students a neural network was hard to justify, and the brief leaves the method open. About 20 seconds.

## Slide 15: How we used generative AI

We used generative AI, mainly Claude Code, throughout the work. It generated much of the code and the notebook text, proposed approaches and selection rules, searched the literature, reviewed our methodology and charts, built these slides and drafted their notes, and answered our conceptual questions. We took the decisions, and we also proposed ideas to the AI about what could be done. We also recorded the use in a log, included in the delivery. The whole presentation is about 10 minutes. About 30 seconds.
