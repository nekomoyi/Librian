export default 調用山彥 = (方法, 參數=[])->
    if 山彥.傳輸 == 'promise'
        return 山彥[方法].apply(山彥, 參數)

    new Promise (完成)->
        山彥[方法].apply(山彥, 參數.concat([完成]))
