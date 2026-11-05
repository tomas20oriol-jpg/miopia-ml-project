# Speaker notes

For the Canva presentation (20 slides), about 9 minutes. Same text as `video_script_en.md`, without timings.

## Slide 1: Predicting myopia in medical students

Ana: Hello, we are Ana and Tomás. We tried to predict myopia in third-year medical students. With only 132 students, the question is not only which model wins, but how much we can trust the result.

## Slide 2: Index

Ana: We start with the problem and the data, then how we prepared it and chose the models, how we used AI, the results and how far to trust them, our conclusions, and the team.

## Slide 3: Four targets, 24 test students

Ana: The brief asks for four predictions for each student: myopia or not; myopia magna, which is more than six dioptres; Combo, which separates control, myopia and magna; and DCombo, which also splits myopia into M1 and M2. Myopia magna matters most, because it can lead to retinal disease, and it is also the rarest class. We deliver labels for 24 test students whose answers we do not have.

## Slide 4: Data overview

Tomás: We have 132 training students with 49 raw columns. Only 10 are labelled myopia magna, so always answering no already gives 92 percent accuracy and finds nobody. That is why accuracy alone cannot rank our models. One feature stands out: axial length, the length of the eye, which rises from 23.5 millimetres in controls to 24.5 in myopia and 26.4 in myopia magna.

## Slide 5: Inconsistent labels

Tomás: We also found 8 students labelled myopia magna in Combo but not in the MM column. Three of their four targets say myopia magna, so we treat the MM column as the error and correct it, which gives 18 magna cases. Their eyes are as long as in the magna group, but their corneas are flatter, so they might really be under six dioptres. We report the correction as a risk.

## Slide 6: Cleaning and new features

Tomás: We turned the 49 raw columns into 32 numeric features. We dropped 21: one empty, twelve that are combinations of others, seven judgement calls, and phototype, which was mixed up with a neighbouring column and unusable for 45 percent of students. Imputation and scaling are fitted inside each training fold. And we added one feature from the medical literature: axial length divided by the corneal radius, because myopia appears when the eye is too long for the power of its cornea.

## Slide 7: Class imbalance

Ana: The classes are unbalanced, so we did four things. Stratified folds, so every fold keeps the rare magna class. Balanced class weights, so rare classes count as much in training. Balanced accuracy and macro-F1 to choose the models, with accuracy always reported. And a tuned threshold for MM, which we tested and which did not beat the default of 0.5. The trap is a model that always says no: it looks accurate, but finds no magna case.

## Slide 8: Validation

Ana: With so little data, validation matters most. Every step that learns from the data sits in a pipeline that is refitted on each training fold, so nothing leaks. We repeat stratified five-fold cross-validation ten times and report the spread, not one number. Tuned models use nested cross-validation, with an inner grid search. And the test set is used once, only to predict.

## Slide 9: Candidate models

Ana: We compared four model families: logistic regression; an SVM with an RBF kernel; a random forest; and XGBoost, which we did not see in class. It builds small trees one after another, each correcting the errors of the previous ones. We also tried two ideas: the axial/corneal ratio, and an ordinal model for DCombo, which respects the order of the classes.

## Slide 10: Decision rule

Ana: We wrote the decision rule before running the models. The reference is the better logistic baseline. A candidate must be clearly better, which means its mean paired gain over the repeats is larger than one standard deviation, through one of two routes, and it must pass again on new folds. Route B was added after seeing validation results, and the report says so.

## Slide 11: How we used generative AI

Tomás: We used generative AI throughout, mainly Claude Code. It wrote much of the code and the notebook text, answered conceptual questions, proposed approaches, and reviewed the methodology and the charts. The decisions were ours.

## Slide 12: Baselines

Ana: The baselines first. Always answering the majority class finds no magna case. Logistic regression on axial length alone is strong: on balanced accuracy, all 32 features do no better on any target. So the better of the two is the bar every model has to beat.

## Slide 13: Model comparison

Ana: Against that bar, tree ensembles won on two targets: XGBoost on MM and the random forest on Combo. The ratio helped M, Combo and DCombo, but not MM, where axial length alone separates the classes better. On the right, the Combo forest relies almost only on axial length and the ratio.

## Slide 14: Final models

Ana: So each target has its own model. M: logistic regression on axial length and the ratio, with balanced accuracy 0.80. MM: XGBoost on the 32 features at the default threshold, with balanced accuracy 0.90 and accuracy 0.96, against 0.86 for always saying no. Combo: the random forest with the ratio, 0.77. DCombo: logistic regression on axial length and the ratio, 0.65.

## Slide 15: Where the models fail

Tomás: Where do the models fail? Mostly between neighbouring classes. In DCombo, 63 percent of predictions are right, 35 percent are one class away and 2 percent further. M1 is the hardest class: it is often called control. The MM model misses about one magna case in six, with very few false alarms.

## Slide 16: How optimistic are the scores

Tomás: We chose these models with the same students who score them, after 44 selection tests, so the scores flatter them. We repeated the whole selection inside the folds. The gain over axial length holds on M and on MM, where XGBoost is chosen in every fold. It disappears on DCombo, and on Combo the repeated selection ends below axial length. With useless information, our test still passes one time in three on Combo, so that choice is weak. The cross-validation scores are an upper range.

## Slide 17: Expected test accuracy

Tomás: This is what we expect on the test set. With 24 students, one student is worth 0.04 of accuracy, and sampling alone moves a score by four or five students. All four targets are expected above the majority class, MM clearly so. One risk: our model says myopia magna for 5 of the 24 test students, more than in training, but compatible with chance. We did not change any label after seeing the test set.

## Slide 18: Conclusions

Ana: To conclude. Simple first: axial length and a logistic regression matched complex models on M and DCombo. Domain knowledge helped: the ratio gave gains, most clearly on M. And measuring our doubt is part of the result. The limits are the data: 132 students, 18 magna cases and no refraction values. More students and a direct measure of refraction would help more than another model.

## Slide 19: Team and tools

Tomás: Tomás and Ana did all the parts together, and the workload was shared fifty-fifty. Our models are built with scikit-learn and XGBoost.

## Slide 20: Thank you

Ana: Thank you for your attention.
