def trans_features(df):
    
    # drop irrelevant features
    drop_list = pd.read_excel('data/old_features_ames.xlsx', usecols="A,D").dropna()['Feature'].tolist()
    df.drop(columns=drop_list, inplace=True)
    
    
    # fill missing values
    ofdf = pd.read_excel('data/old_features_ames.xlsx', usecols="A,B,C,F")
    ofdf = ofdf[~ofdf['Feature'].isin(drop_list)]
    ofdf.dropna(inplace=True) #only target 'SalePrice' has NaN for 'Missing Handle'
    median_list = ofdf[ofdf['Missing Handle']=='median']['Feature'].tolist()
    mode_list = ofdf[ofdf['Missing Handle']=='mode']['Feature'].tolist()
    
    for med in median_list:
        df[med].fillna(df[med].median(), inplace=True)
    
    for mod in mode_list:
        df[mod].fillna(df[mod].mode()[0], inplace=True)
    
    cusdf = pd.read_excel('data/old_features_ames.xlsx', usecols="A,G")
    cusdf.dropna(inplace=True)
    for index, row in cusdf.iterrows():
        df[row['Feature']].fillna(row['Missing Custom'], inplace=True)
    
    
    # transformations
    log_list = ['LotFrontage','LotArea','MasVnrArea','BsmtFinSF1','BsmtFinSF2','TotalBsmtSF','1stFlrSF','GrLivArea']
    for logf in log_list:
        df[logf] = df[logf].apply(lambda x: np.log(x+1))
    
    mssubclass_mapper = {
        20 : 'mssub1',
        30 : 'mssub2',
        40 : 'mssub3',
        45 : 'mssub4',
        50 : 'mssub5',
        60 : 'mssub6',
        70 : 'mssub7',
        75 : 'mssub8',
        80 : 'mssub9',
        85 : 'mssub10',
        90 : 'mssub11',
        120 : 'mssub12',
        150 : 'mssub13',
        160 : 'mssub14',
        180 : 'mssub15',
        190 : 'mssub16'
    }

    mosold_mapper = {
        1 : 'january',
        2 : 'february',
        3 : 'march',
        4 : 'april',
        5 : 'may',
        6 : 'june',
        7 : 'july',
        8 : 'august',
        9 : 'september',
        10 : 'october',
        11 : 'november',
        12 : 'december'
    }

    df['MSSubClass'].replace(mssubclass_mapper, inplace=True)
    df['MoSold'].replace(mosold_mapper, inplace=True)
    
    df['GarageYrBlt'] = df['GarageYrBlt']-1890
    
    def change_categories(x, cat_dict):
        if x in cat_dict.keys():
            return cat_dict[x]
        elif 'rare_cat_name' in cat_dict.keys():
            return cat_dict['rare_cat_name']
        else:
            return 'others'
    
    
    df['MSZoning'] = df['MSZoning'].apply(lambda x: change_categories(x, {'RL':'RL','FV':'FV'}))
    df['LotShape'] = df['LotShape'].apply(lambda x: change_categories(x, {'Reg':'Reg','rare_cat_name':'Irreg'}))
    df['LandContour'] = df['LandContour'].apply(lambda x: change_categories(x, {'Lvl':'Lvl','Bnk':'Bnk'}))
    df['LotConfig'] = df['LotConfig'].apply(lambda x: change_categories(x, {'Inside':'Inside','FR2':'FR2','Corner':'Corner','rare_cat_name':'CulDFR3'}))
    df['Neighborhood'] = df['Neighborhood'].apply(lambda x: change_categories(x, {'Blmngtn': 'nhood2',  'Blueste': 'nhood3',  'BrDale': 'nhood3',  'BrkSide': 'nhood3',  'ClearCr': 'nhood2',  'CollgCr': 'nhood2',  'Crawfor': 'nhood2',  'Edwards': 'nhood3',  'Gilbert': 'nhood2',  'IDOTRR': 'nhood3',  'MeadowV': 'nhood3',  'Mitchel': 'nhood3',  'NAmes': 'nhood3',  'NPkVill': 'nhood3',  'NWAmes': 'nhood2',  'NoRidge': 'nhood1',  'NridgHt': 'nhood1',  'OldTown': 'nhood3',  'SWISU': 'nhood3',  'Sawyer': 'nhood3',  'SawyerW': 'nhood2',  'Somerst': 'nhood2',  'StoneBr': 'nhood1',  'Timber': 'nhood2',  'Veenker': 'nhood2'}))
    df['Exterior1st'] = df['Exterior1st'].apply(lambda x: change_categories(x, {'AsbShng': 'Ext1_low',  'AsphShn': 'Ext1_low',  'BrkComm': 'Ext1_low',  'BrkFace': 'Ext1_low',  'CBlock': 'Ext1_low',  'CemntBd': 'Ext1_high',  'HdBoard': 'Ext1_low',  'ImStucc': 'Ext1_high',  'MetalSd': 'Ext1_low',  'Plywood': 'Ext1_low',  'Stone': 'Ext1_high',  'Stucco': 'Ext1_low',  'VinylSd': 'Ext1_high',  'Wd Sdng': 'Ext1_low',  'WdShing': 'Ext1_low'}))
    df['Exterior2nd'] = df['Exterior2nd'].apply(lambda x: change_categories(x, {'AsbShng': 'Ext2_low',  'AsphShn': 'Ext2_low',  'Brk Cmn': 'Ext2_low',  'BrkFace': 'Ext2_low',  'CBlock': 'Ext2_low',  'CmentBd': 'Ext2_high',  'HdBoard': 'Ext2_low',  'ImStucc': 'Ext2_high',  'MetalSd': 'Ext2_low',  'Other': 'Ext2_high',  'Plywood': 'Ext2_low',  'Stone': 'Ext2_low',  'Stucco': 'Ext2_low',  'VinylSd': 'Ext2_high',  'Wd Sdng': 'Ext2_low',  'Wd Shng': 'Ext2_low'}))
    df['BldgType'] = df['BldgType'].apply(lambda x: change_categories(x, {'1Fam':'1Fam','TwnhsE':'TwnhsE'}))
    df['HouseStyle'] = df['HouseStyle'].apply(lambda x: change_categories(x, {'1Story':'1Story','1.5Fin':'1.5Fin','2Story':'2Level','2.5Fin':'2Level','rare_cat_name':'other_style'}))
    df['RoofStyle'] = df['RoofStyle'].apply(lambda x: change_categories(x, {'Hip':'Hip','Shed':'Hip','rare_cat_name':'Gable'}))
    df['MasVnrType'] = df['MasVnrType'].apply(lambda x: change_categories(x, {'BrkFace':'Brick','None':'None','BrkCmn':'Brick','Stone':'Stone'})).value_counts()
    df['ExterQual'] = df['ExterQual'].apply(lambda x: change_categories(x, {'Po':1,'Fa':2,'TA':3,'Gd':4,'Ex':5}))
    df['ExterCond'] = df['ExterCond'].apply(lambda x: change_categories(x, {'Po':1,'Fa':2,'TA':3,'Gd':4,'Ex':5}))
    df['Foundation'] = df['Foundation'].apply(lambda x: change_categories(x, {'PConc':'PConc','Wood':'PConc','CBlock':'CBlock','Stone':'CBlock','BrkTil':'BrkTil','Slab':'BrkTil'}))
    df['BsmtQual'] = df['BsmtQual'].apply(lambda x: change_categories(x, {'Po':1,'Fa':2,'TA':3,'Gd':4,'Ex':5}))
    df['HeatingQC'] = df['HeatingQC'].apply(lambda x: change_categories(x, {'Po':1,'Fa':2,'TA':3,'Gd':4,'Ex':5}))
    df['Electrical'] = df['Electrical'].apply(lambda x: change_categories(x, {'SBrkr':'SBrkr','rare_cat_name':'FuseBox'}))
    df['KitchenQual'] = df['KitchenQual'].apply(lambda x: change_categories(x, {'Po':1,'Fa':2,'TA':3,'Gd':4,'Ex':5}))
    df['FireplaceQu'] = df['FireplaceQu'].apply(lambda x: change_categories(x, {'Po':1,'Fa':2,'TA':3,'Gd':4,'Ex':5}))
    df['GarageType'] = df['GarageType'].apply(lambda x: change_categories(x, {'Attchd':'Attchd','BuiltIn':'BuiltIn','Detchd':'Detchd','Basment':'Detchd','2Types':'Detchd','NoGarage':'NoGarage','CarPort':'NoGarage'}))
    df['Fence'] = df['Fence'].apply(lambda x: change_categories(x, {'NoFence':'NoFence','GdPrv':'NoFence','rare_cat_name':'MnPrv'}))
    df['SaleType'] = df['SaleType'].apply(lambda x: change_categories(x, {'New':'New','Con':'New','rare_cat_name':'WD'}))
    df['SaleCondition'] = df['SaleCondition'].apply(lambda x: change_categories(x, {'Normal':'Normal','Partial':'Partial','rare_cat_name':'Abnormal'}))
    
    return df