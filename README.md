# ItemSearcher

Great thanks to [ten-miles-away](https://github.com/ten-miles-away) and his [itemFinder](https://github.com/ten-miles-away/itemFinder)

and also thanks his help in this plugin

ONLY FOR [MCDReforged](https://github.com/Fallen-Breath/MCDReforged/tree)

## Usage / 使用方法

1. 需要[MinecraftItemAPI](https://github.com/Forgot-Dream/MinecraftItemAPI)和[PlayerInfoAPI](https://github.com/TISUnion/PlayerInfoAPI)作为前置 / Need [MinecraftItemAPI](https://github.com/Forgot-Dream/MinecraftItemAPI) and [PlayerInfoAPI](https://github.com/TISUnion/PlayerInfoAPI) 
2. 复制`ItemSearcher.py`到`/plugins` | copy `ItemSearcher.py` to `/plugins`
3. 重载MCDR | Reload MCDR

## Command / 命令

`!!IS` 显示帮助信息



`!!IS search [<Item>]`

搜索名字为`<Item>`的物品，如果无法搜索到官方名，将启用模糊搜索，如果`<item>`为空则默认搜索手持的物品



`!!IS add <Item/hand>] [<Item_cn>] [-f]`

添加`<Item/hand>`[此值为hand时默认获取手上物品id到数据库]，`<Item_cn>`为官方中文名，请手动添加。`[-f]`为可选参数，如果命令带该参数，则强制添加该物品



`!!IS override pos [<Item>]`
 
重写数据库中的`<Item>`(如果<Item>为空则默认获取玩家手持的物品)的坐标为玩家当前位置



`!!IS override nick [<add/remove>] [<Item_name/hand>] [<Nick>]`
 
添加/移除`<Item_name/hand>`的`<Nick>(常用名)



`!!IS override nick list [<Item_name/hand>]`
 
列出`<Item_name/hand>`的常用名



`!!IS override name_cn [<item/hand>] [<name_cn>]`
 
重写`[<item/hand>]`的中文名为`[<name_cn>]`



`!!IS data [<hand/item_name>]`
 
 获取`[<hand/item_name>]`的数据
