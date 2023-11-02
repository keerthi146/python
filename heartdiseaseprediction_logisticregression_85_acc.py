# -*- coding: utf-8 -*-
"""heartdiseaseprediction-logisticregression-85-acc.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mFixnToHYrScSnacxhDpnszK83lxc90I
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
print("Setup Complete")

"""# Load the Dataset"""

# Read the file into a variable heart
heart= pd.read_csv('/content/dataset_heart.csv')

"""## Exploratory Data Analysis

### Explore the Data: Get a basic understanding of the dataset.
"""

heart.head()

heart.info()

# print the number of rows and columns
print("Number of Rows: ", heart.shape[0])
print("Number of Columns: ", heart.shape[1])

heart.isnull().sum()

heart.isnull().sum().sum()

heart.describe().T.style.background_gradient(cmap = "Blues")

"""### Data Visualization: Create visualizations to understand the data."""

heart.columns

#Take the column values
names = ['age', 'sex ', 'chest pain type', 'resting blood pressure',
       'serum cholestoral', 'fasting blood sugar',
       'resting electrocardiographic results', 'max heart rate',
       'exercise induced angina', 'oldpeak', 'ST segment', 'major vessels',
       'thal', 'heart disease']

# Set the custom font sizes
plt.rc('font', size=14)
plt.rc('axes', labelsize=14, titlesize=14)
plt.rc('legend', fontsize=14)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)

# Create the box plots
heart.plot(kind='box', subplots=True, layout=(4, 4), sharex=False, sharey=False, figsize=(8, 8), y=names)

# Adjust the layout and spacing
plt.tight_layout()
plt.show()

# extra code – the next 5 lines define the default font sizes
plt.rc('font', size=14)
plt.rc('axes', labelsize=14, titlesize=14)
plt.rc('legend', fontsize=14)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)

heart.hist(bins=50, figsize=(14, 14))

plt.show()

sns.pairplot(heart,hue='heart disease')

# Identify duplicate rows
heart[heart.duplicated()]

"""### Target Class Analysis"""

# checking the distribution of Target Variable
print(heart['heart disease'].value_counts())

plt.figure(figsize=(13,8),dpi=150)
ax = sns.countplot(data=heart, x='heart disease', palette="Set2")
for p in ax.patches:
    x=p.get_bbox().get_points()[:,0]
    y=p.get_bbox().get_points()[1,1]
    ax.annotate('{:.1f}%'.format(100.*y/len(heart)), (x.mean(), y),
            ha='center', va='bottom')

"""# Spliting Independent And Dependent features"""

X=heart.drop('heart disease',axis=1)
y=heart['heart disease']

X

y

"""### Looking for Correlation"""

corr_matrix = X.corr()

import seaborn as sns
plt.figure(figsize = (14,10))
sns.heatmap(corr_matrix, annot = True, cmap = 'BuGn')
plt.show()

"""### Bivariate Analysis"""

plt.figure(figsize=(12,8))
ax = sns.scatterplot(x='oldpeak',y='ST segment',data=heart,hue='heart disease',s=200,alpha=0.9,palette='Set2')
plt.legend(bbox_to_anchor=(1.2,0.5),title="heart disease")

"""# Stratified Train Test Split Data"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 42, stratify = y)

X_train

print(X.shape, X_train.shape, X_test.shape)

"""# Data Preprocessing

### Standard Scaler
"""

from sklearn.preprocessing import StandardScaler
df2 = heart.copy()
ss = StandardScaler()
df2[['age', 'resting blood pressure','serum cholestoral', 'max heart rate','oldpeak']] = ss.fit_transform(df2[['age','resting blood pressure','serum cholestoral', 'max heart rate','oldpeak']])

"""### Handling Outliers"""

for col in heart.columns:
    if heart[col].dtypes != 'object':
        lower_limit, upper_limit = heart[col].quantile([0.25,0.75])
        IQR = upper_limit - lower_limit
        lower_whisker = lower_limit - 1.5 * IQR
        upper_whisker = upper_limit + 1.5 * IQR
        heart[col] = np.where(heart[col]>upper_whisker,upper_whisker,np.where(heart[col]<lower_whisker,lower_whisker,heart[col]))

"""# Model Training & Evaluation"""

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

knn =KNeighborsClassifier(n_neighbors=5)
logreg = LogisticRegression()
dt = DecisionTreeClassifier(random_state=0)
rf = RandomForestClassifier()

knn.fit(X_train, y_train)
logreg.fit(X_train, y_train)
dt.fit(X_train, y_train)
rf.fit(X_train, y_train)

from sklearn.metrics import accuracy_score

y_pred = knn.predict(X_test)
print('K-Nearest Neighbors  Test Accuracy ', accuracy_score(y_test, y_pred ))

y_pred = logreg.predict(X_test)
print('Logistic Regression Test Accuracy ', accuracy_score(y_test, y_pred ))

y_pred = dt.predict(X_test)
print('Decision Tree Test Accuracy ', accuracy_score(y_test, y_pred ))

y_pred = rf.predict(X_test)
print('Random Forest Test Accuracy ', accuracy_score(y_test, y_pred ))

"""# Classification Report before Hyperparameter Tuning"""

from sklearn.metrics import classification_report

def plot_classification_report(y_train, y_pred1, y_test, y_pred2, c_name):
    print("-"*25,c_name,"(TRAIN SET)","-"*25)
    print(classification_report(y_train, y_pred1))
    print("-"*25,c_name,"(Test SET)","-"*25)
    print(classification_report(y_test, y_pred2))

c_name= "K-Nearest Neighbors"
plot_classification_report(y_train, knn.predict(X_train), y_test, knn.predict(X_test), c_name)

c_name= "Logistic Regression"
plot_classification_report(y_train, logreg.predict(X_train), y_test, logreg.predict(X_test), c_name)

c_name= "Decision Tree"
plot_classification_report(y_train, dt.predict(X_train), y_test, dt.predict(X_test), c_name)

c_name= "Random Forest"
plot_classification_report(y_train, rf.predict(X_train), y_test, rf.predict(X_test), c_name)