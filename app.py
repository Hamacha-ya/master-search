from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
from pandas.io import parsers
import streamlit as st
import mojimoji
from streamlit.caching import cache

st.title('製品情報問合せ検索アプリ')

st.sidebar.write("""
# ファジー検索
品名と思われる文字を入力するとファジー理論による検索値の高い順に表示されます。
連続で書いてもスペース入れても間違っててもなんでもＯＫ
""")

@st.cache
def read_csv():
    nykf = pd.read_csv('./file/NYKF.csv', sep=',', index_col=0)
    nykf = nykf.sort_values(by=['工順'], ascending=[False])
    nycf = pd.read_csv('./file/NYCF.csv', sep=',', index_col=0)
    nycf2 = pd.read_csv('./file/NYCF.csv', sep=',', index_col=2)    
    df_list = pd.read_csv('./file/YF.csv', sep=',')
    return df_list,nykf,nycf,nycf2

df_list,nykf,nycf,nycf2 = read_csv()
lastrow = len(df_list)

code = st.sidebar.text_input('品名部位を入力 半角全角、大小文字OK', '')
code2 = st.sidebar.text_input('部品コードを入力 半角のみ 大小文字は正確に', '')
buhincode1 = ''
buhincode2 = ''

st.sidebar.write("""
## 検索値マッチ率(%)
""")
match = st.sidebar.slider('率', 30, 80, 50)

st.sidebar.write("""
## 表示件数
""")
display = st.sidebar.slider('件数', 5, 20, 10)

st.sidebar.write('データ更新日:2021-05-31')
st.sidebar.write('Ver.1.000.02')


df2 = pd.DataFrame({'部番': [], '品名': [], 'マッチ率': []})

if code != '':
    comment = st.empty()
    comment.write('Hold the line, please')
    code = code.upper()
    input_txt = mojimoji.han_to_zen(code)
    
    #for i in range(0,lastrow):
    for i in range(0,lastrow):
        #検索部位OCRとマスターを照合
        try:
            s = fuzz.ratio(input_txt , df_list.iloc[i,1])
        except:
            pass

        if s > match:  #マッチ率より上        
            df2 = df2.append({'部番': df_list.iloc[i,0], '品名': df_list.iloc[i,2], 'マッチ率': s}, ignore_index=True)

    if len(df2) > 0:
        comment.write('')
        df2 = df2.sort_values(by='マッチ率',ascending=False).reset_index(drop=True)
        st.write(df2.head(display))
    
    buhincode1 = st.multiselect(
                '部品コードを選択してください。',
                list(df2['部番'][:display]))



if code2 != '':
    #input_txt = mojimoji.han_to_zen(code)
    input_txt = code2

    for i in range(0,lastrow):
        #検索部位OCRとマスターを照合
        s = fuzz.ratio(input_txt , df_list.iloc[i,0])
        
        if s > match:  #マッチ率50%より上        
            df2 = df2.append({'部番': df_list.iloc[i,0], '品名': df_list.iloc[i,2], 'マッチ率': s}, ignore_index=True)

    if len(df2) > 0:
        df2 = df2.sort_values(by='マッチ率',ascending=False).reset_index(drop=True)
        st.write(df2.head(display))

    buhincode2 = st.multiselect(
                '部品コードを選択してください。',
                list(df2['部番'][:display]))

if buhincode1 != '':
    try:
        st.write('構成情報')
        st.write(nycf.loc[buhincod1])
    except:
        pass
    try:
        st.write('工程情報')
        st.write(nykf.loc[buhincode1])
    except:
        pass
    try:
        st.write('共通部品')
        st.write(nycf2.loc[buhincode1])
    except:
        pass

if buhincode2 != '':
    try:
        st.write('構成情報')
        st.write(nycf.loc[buhincode2])
    except:
        pass
    try:
        st.write('工程情報')
        st.write(nykf.loc[buhincode2])
    except:
        pass
    try:
        st.write('共通部品')
        st.write(nycf2.loc[buhincode2])
    except:
        pass