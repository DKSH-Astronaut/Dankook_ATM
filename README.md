<div align="center">
<img src="img/astro.png">
<h1><b>Dankook Software High School - ATM</b></h1>
<p>ATM with LRU-Cache + Self Encryption + Linear regression</p>
<img src="https://img.shields.io/badge/Python-v3-blue.svg">
<img src="https://img.shields.io/github/license/DKSH-Astronaut/Dankook_ATM?style=flat">
<img src="https://img.shields.io/github/last-commit/DKSH-Astronaut/Dankook_ATM">
</div>
<br>

# 1. Introduction

ATM is an electronic communication device that allows customers of financial institutions to directly engage in financial transactions such as cash withdrawals, deposits, fund transfers, books and account information at any time through bank employees.

We made a ATM system using Python 3.
We are working on this project to develop ATM to learn the same functions as cache memory, write clean codes, and think and grow with team members.
The ATM has created functions such as register, login, deposit, withdrawal, loan, transfer, balance inquiry, credit inquiry, customized recommendation system, etc.
To create these features, we implemented encryption, simple linear regression, and LRU cache memory to create more complete ATM.

# 2. Modules

## 1. astro_base64.py
## 2. astro_secret.py
## 3. linear_regression.py
<h3><b>1. Introduction</b></h3>
Regression is a data analysis method in which the dependent variable Y is represented by the different variables X1,.., and Xp.
The response variable is an explanatory variable, and the variables used for explanation are called independent variables.
Regression analysis is intended to logically explain the prediction of a response variable by an independent variable or the relationship between an independent variable and a response variable.

<h2><b>4. LRUCache.py</b></h2>
<h3><b>1. Introduction</b></h3>
Cache memory is a high-speed semiconductor memory that is installed between CPU and main memory.

It is often useful to have these things in memory.
Of course, it is desirable to ensure that the capacity of cache memory does not become too large, as it slows down as capacity increases.

This module provides such a cache.

In most cases, the following may be used:

<h3><b>2. How to use this module</b></h3>

Default nodeMap form : **`nodeMap = {key: [value, count]}`**

The functions of the module are as follows.

| what it does              |      FUnc       |                             Remark |
| :------------------------ | :-------------: | ---------------------------------: |
| Search value in the Queue |    get(key)     |              Return value in 'key' |
| Put value in the Queue    | put(key, value) | Add 'value' corresponding to 'key' |

```python
from LRUCache import *  # import module

lru = LRUCache(2)   # Set Cache Size (args: int)

lru.put(1, 1)   # put(key, value)
print(lru.get(1))   # get(key)
print(lru.nodeMap)  # print nodeMap
```

This is a simple use.<br>
An example of using this is as follows.

<h3><b>Example:</b></h3>

```python
from LRUCache import *

lru = LRUCache(2)

if __name__ == "__main__":
    lru.put(1, 1)
    lru.put(2, 2)
    print(lru.get(1))   # returns 1
    lru.put(3, 3)   # evicts key 2
    print(lru.get(2))   # returns -1 (not found)
    lru.put(4, 4)   # evicts key 1
    print(lru.get(1))   # returns -1 (not found)
    print(lru.get(3))   # returns 3
    print(lru.get(4))   # returns 4
    print(lru.nodeMap)  # show nodeMap
```

<h3><b>3. When does cache eviction occur?</b></h3>

By default, this cache only expires each time an item is stabbed, and all methods in this class are cleaned up.
