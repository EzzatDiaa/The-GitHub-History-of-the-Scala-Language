# ## 1. Scala's real-world project repository data

# Importing pandas
import pandas as pd

# Loading in the data
pulls_one = pd.read_csv('datasets/pulls_2011-2013.csv')
pulls_two = pd.read_csv('datasets/pulls_2014-2018.csv')
pull_files = pd.read_csv('datasets/pull_files.csv')


# In[40]:

get_ipython().run_cell_magic('nose', '', '\nimport pandas as pd\n\ndef test_pulls_one():\n    correct_pulls_one = pd.read_csv(\'datasets/pulls_2011-2013.csv\')\n    assert correct_pulls_one.equals(pulls_one), \\\n    "Read in \'datasets/pulls_2011-2013.csv\' using read_csv()."\n\ndef test_pulls_two():\n    correct_pulls_two = pd.read_csv(\'datasets/pulls_2014-2018.csv\')\n    assert correct_pulls_two.equals(pulls_two), \\\n   "Read in \'datasets/pulls_2014-2018.csv\' using read_csv()."\n    \ndef test_pull_files():\n    correct_pull_files = pd.read_csv(\'datasets/pull_files.csv\')\n    assert correct_pull_files.equals(pull_files), \\\n    "Read in \'pull_files.csv\' using read_csv()."')


# ## 2. Preparing and cleaning the data
# In[41]:

pulls = pulls_one.append([pulls_two], ignore_index=True)
pulls.info()

pulls['date'] = pd.to_datetime(pulls['date'], utc=True)



get_ipython().run_cell_magic('nose', '', "\n# one or more tests of the students code. \n# The @solution should pass the tests.\n# The purpose of the tests is to try to catch common errors and to \n# give the student a hint on how to resolve these errors.\n\ndef test_pulls_length():\n    assert len(pulls) == 6200, \\\n    'The DataFrame pulls does not have the correct number of rows. Did you correctly append pulls_one to pulls_two?'\n\ndef test_pulls_type():\n    assert type(pulls['date'].dtype) is pd.core.dtypes.dtypes.DatetimeTZDtype, \\\n    'The date for the pull requests is not the correct type.'")


# ## 3. Merging the DataFrames

data = pulls.merge(pull_files, on='pid')


# In[44]:

get_ipython().run_cell_magic('nose', '', '\n# one or more tests of the students code. \n# The @solution should pass the tests.\n# The purpose of the tests is to try to catch common errors and to \n# give the student a hint on how to resolve these errors.\n\ndef test_merge():\n    assert len(data) == 85588, \\\n    \'The merged DataFrame does not have the correct number of rows.\'\n\ndef test_merge_dataframes():\n    correct_data = pulls.merge(pull_files, on=\'pid\')\n    also_correct_data = pull_files.merge(pulls, on=\'pid\')\n    assert correct_data.equals(data) or \\\n        also_correct_data.equals(data), \\\n        "The DataFrames are not merged correctly."        ')


# ## 4. Is the project still actively maintained?
# In[45]:

get_ipython().run_line_magic('matplotlib', 'inline')
data['month'] = data['date'].dt.month
data['year'] = data['date'].dt.year
counts = data.groupby(['month', 'year'])['pid'].count()
counts.plot(kind='bar', figsize = (12,4))

# In[46]:

get_ipython().run_line_magic('matplotlib', 'inline')
by_user = data.groupby('user').agg({'pid': 'count'})
by_user.hist()




# In[47]:

last_10 = pulls.sort_values(by = 'date').tail(10)
last_10
joined_pr = pull_files.merge(last_10, on='pid')
files = set(joined_pr['file'])
files



# ## 7. Who made the most pull requests to a given file?
# In[48]:

# This is the file we are interested in:
file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'
file_pr = data[data['file'] == file]
author_counts = file_pr.groupby('user').count()
author_counts.nlargest(3, 'file')




# ## 8. Who made the last ten pull requests on a given file?
# In[49]:
file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

file_pr = pull_files[pull_files['file'] == file]

joined_pr = pulls.merge(file_pr, on='pid')

users_last_10 = set(joined_pr.nlargest(10, 'date')['user'])


users_last_10




#  The pull requests of two special developers
# In[50]:
get_ipython().run_line_magic('matplotlib', 'inline')
authors = ['xeno-by', 'soc']
by_author = pulls[pulls['user'].isin(authors)]
counts = by_author.groupby([by_author['user'], by_author['date'].dt.year]).agg({'pid': 'count'}).reset_index()
counts_wide = counts.pivot_table(index='date', columns='user', values='pid', fill_value=0)

# ## 10. Visualizing the contributions of each developer

authors = ['xeno-by', 'soc']
file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'
by_author = data[data['user'].isin(authors)]
by_file = by_author[by_author['file'] == file]
grouped = by_file.groupby(['user', by_file['date'].dt.year]).count()['pid'].reset_index()
by_file_wide = grouped.pivot_table(index='date', columns='user', values='pid', fill_value=0)
by_file_wide.plot(kind='bar')




