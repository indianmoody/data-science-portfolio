## Ames Housing Project Timeline

* Drop 'Id', 'PoolQC': almost all values under single category: too much imbalanced.
* Convert 'MSSubClass' into categorical from numerical.
* 










### New Features:

* Remodelling : 'no' if 'YearRemodAdd' - 'YearBuilt' == 0 else 'yes'; before transformation of these two features
* LotAvailable: 'no' if 'LotArea' == 0 else 'yes'. zero LotArea means house is not on ground floor. before transformation.
* 