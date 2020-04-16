# -*- coding: utf-8 -*-   

import yaml
import json
import os

Prefix = '!!IS'
ConfigFileFolder = 'config/'
ConfigFilePath = ConfigFileFolder + 'ItemSearcher.yml'

HelpMessage = '''------Item Searcher------
一个智能的§a仓储§c管理§r插件
§a【格式说明】§r
§7{0}§r 显示帮助信息

§7{0} search §e[<Item>]
§r搜索名字为§e<item>§r的物品，如果无法搜索到官方名，将启用模糊搜索，如果§e<item>§r为空则默认搜索手持的物品

§7{0} add §e[<Item/hand>] [<Item_cn>] [-f]
§r添加§e<Item/hand>§r§o§7此值为hand时默认获取手上物品id§r到数据库，§e<Item_cn>§r为官方中文名，请手动添加。§e[-f]§r为可选参数，如果命令带该参数，则强制添加该物品

§7{0} override pos §e[<Item>]
§r重写数据库中的§e<Item>§o§7(如果<Item>为空则默认获取玩家手持的物品)§r的坐标为玩家当前位置

§7{0} override nick §e[<add/remove>] [<Item_name/hand>] [<Nick>]
§r添加/移除§e<Item_name/hand>§r的§e<Nick>(常用名)

§7{0} override nick list §e[<Item_name/hand>]
§r列出§e<Item_name/hand>§r的常用名

§7{0} override name_cn §e[<item/hand>] [<name_cn>]
§r重写§e[<item/hand>]§r的中文名为§e[<name_cn>]

§7{0} data §e[<hand/item_name>]§r获取§e[<hand/item_name>]§r的数据
§a【例子】§r
§7{0} search 地毯
§7{0} add hand 钻石
§7{0} add firework_rocket_1 烟花火箭一级 -f
§7{0} override pos hand
§7{0} override nick add/remove white_carpet 白地毯
§7{0} override nick list hand
§7{0} override name_cn white_carpet 白色地毯
§7{0} data hand
'''.format(Prefix)

For_All = True

def on_load(server ,old):
    server.add_help_message('!!IS','物品查找器')
    if not os.path.isfile(ConfigFilePath):
        server.logger.info('[IS] 未找到配置文件，已自动生成')
        with open(ConfigFilePath, 'w+') as f:
            f.close()

def pos_print(server, player, pos_x, pos_y, pos_z, name_cn, glowing):# 打印坐标
    server.tell(player,'[IS] §e' + name_cn + ' §r在[x:{} ,y:{} ,z:{} ,dim:0]'.format(pos_x,pos_y,pos_z))
    if glowing:
        server.tell(player, '[IS]已为您进行十五秒的高亮')
        server.execute('summon minecraft:falling_block ' + str(pos_x) + ' ' + str(pos_y) + ' ' + str(pos_z) +' {CustomNameVisible:1b,Glowing:1b,NoGravity:1b,ActiveEffects:[{Id:14,Amplifier:254,Duration:600,ShowParticles:0b}],Time:1,DropItem:0b,HurtEntities:0b,BlockState:{Name:"minecraft:glass"}}')


def print_message(server, player, message, for_all):    # 分行打印各种信息
    for each in message.splitlines():
        if for_all:
            server.say('[IS]' + each)
        else:
            server.tell(player, '[IS]' + each)


def config_data():  # 返回配置文件中的数据 [重复太多遍，看的太难受了]
    with open(ConfigFilePath, 'r', encoding='UTF-8') as yml:
        y = yaml.safe_load_all(yml)
        data_list = []
        for data in y:
            data_list.append(data)
            yml.close()
    return data_list


def dump_yaml(data_list, data):  # 把data合到data_list中去然后更新配置文件 [重复太多遍，看的太难受了]
    with open(ConfigFilePath, 'w', encoding='UTF-8') as yml:
        data_list.append(data)
        yaml.safe_dump_all(data_list, yml, allow_unicode=True)
        yml.close()


def item_add_nickname(server, player, item, nick_name):  # [item:官方英文名，nick_name:新nickname] 增加nickname
    data_list = config_data()
    for i in range(len(data_list)):
        name = data_list[i]['name']
        if item == name:
            data = data_list[i]
            if nick_name in data['nick_name']:
                print_message(server, player, '该常用名已存在', For_All)
                return -1
            del data_list[i]
            if data['nick_name'] == ['']:
                data['nick_name'] = [nick_name]
            else:
                data['nick_name'].append(nick_name)
            dump_yaml(data_list, data)
            print_message(server, player, '已更新 §e' + data['name'] + ' §r的常用名', For_All)
            return 0


def item_del_nickname(server, player, item, nick_name):  # [item:官方英文名，nick_name:旧nickname] 删除nickname
    data_list = config_data()
    for i in range(len(data_list)):
        name = data_list[i]['name']
        if item == name:
            data = data_list[i]
            if nick_name not in data['nick_name']:
                print_message(server, player, '该常用名不存在', For_All)
                nickname_list(server, player, data['name'])
                return -1
            del data_list[i]
            if len(data['nick_name']) == 1:
                data['nick_name'] = ['']
            else:
                data['nick_name'].remove(nick_name)
            dump_yaml(data_list, data)
            print_message(server, player, '已更新 §e' + data['name'] + ' §r的常用名', For_All)
            return 0


def item_change_name_cn(server, player, item, name_cn):  # [item:官方英文名，nick_cn:新中文名] 改写中文名
    data_list = config_data()
    for i in range(len(data_list)):
        name = data_list[i]['name']
        if item == name:
            data = data_list[i]
            del data_list[i]
            data['name_cn'] = name_cn
            dump_yaml(data_list, data)
            print_message(server, player, '已更新 §e' + data['name'] + ' §r的中文名：' + data['name_cn'], For_All)
            return 0


def nickname_list(server, player, item):  # [item:官方英文名] 返回一个list,包含所有nick_name,无nick_name返回空list
    data_list = config_data()
    for i in range(len(data_list)):
        name = data_list[i]['name']
        if item == name:
            nick_list = data_list[i]['nick_name']
            if nick_list == ['']:
                print_message(server, player, '§e ' + data_list[i]['name'] + '/' + data_list[i]['name_cn'] + ' §r无常用名', For_All)
                return []
            else:
                print_message(server, player, '§e ' + data_list[i]['name'] + '/' + data_list[i]['name_cn'] + ' §r的常用名有：', For_All)
                nick = ''
                for each in nick_list:
                    nick += each + '  '
                print_message(server, player, nick, For_All)
                return nick_list


def official_name(item):  # [item:官方中文名或官方英文名] 返回官方英文名,无匹配返回None,用来给上面的函数喂参数
    data_list = config_data()
    for i in range(len(data_list)):
        if item == data_list[i]['name']:
            return item
        if item == data_list[i]['name_cn']:
            return data_list[i]['name']
    return None


def print_item_data(server, player, item):      # [item:官方英文名] 打印所有信息
    data_list = config_data()
    for i in range(len(data_list)):
        if item == data_list[i]['name']:
            message = data_list[i]['name'] + '''的配置文件：
中文名：''' + data_list[i]['name_cn'] + '''
常用名：'''
            for each in data_list[i]['nick_name']:
                if each != '':
                    message += each + '''  '''
            message += '''
坐标：[x:''' + str(data_list[i]['pos_x']) + ''' ,y:''' + str(data_list[i]['pos_y']) + ''' ,z:''' + str(data_list[i]['pos_z']) + ''' ,dim:0]'''
            print_message(server, player, message, For_All)
    
def name_search(server, Name, player, respond_search):
    data_list = config_data()
    counter = 0
    for i in range(len(data_list)): #中文名匹配
        name = data_list[i]["name_cn"]
        if Name == name:
            pos_x = data_list[i]["pos_x"]
            pos_y = data_list[i]["pos_y"]
            pos_z = data_list[i]["pos_z"]
            name_cn = data_list[i]["name_cn"]
            if respond_search:
                pos_print(server, player, pos_x, pos_y, pos_z, name_cn, True)
            return
    i = None
    for i in range(len(data_list)):  #英文id匹配
        name = data_list[i]["name"]
        if Name == name:
            pos_x = data_list[i]["pos_x"]
            pos_y = data_list[i]["pos_y"]
            pos_z = data_list[i]["pos_z"]
            name_cn = data_list[i]["name_cn"]
            if respond_search:
                pos_print(server, player, pos_x, pos_y, pos_z, name_cn, True)
            return True
    i = None            
    for i in range(len(data_list)):  #模糊搜索
        nick = data_list[i]["nick_name"]
        nick_str = ','.join(nick)
        if not nick_str.find(Name) == -1:
            pos_x = data_list[i]["pos_x"]
            pos_y = data_list[i]["pos_y"]
            pos_z = data_list[i]["pos_z"]
            name_cn = data_list[i]["name_cn"]
            counter += 1
            if respond_search:
                pos_print(server, player, pos_x, pos_y, pos_z, name_cn, False)
    if counter == 0:
        if respond_search:
            server.tell(player,'[IS]无法在数据库中找到该物品')
        return False
             
             
def item_add(name, pos_x, pos_y, pos_z, name_cn ,server): #物品添加
    data_list = config_data()
    dump_yaml(data_list,{'name': name, 'name_cn': name_cn, 'pos_x': pos_x, 'pos_y': pos_y, 'pos_z': pos_z, 'nick_name': ['']})
        
        
def get_item_name(server, player):# get玩家手上物品
    api = server.get_plugin_instance('PlayerInfoAPI')
    SelectedItemSlot = api.getPlayerInfo(server, player, path='SelectedItemSlot')
    Inventory =  api.getPlayerInfo(server, player, path='Inventory[{Slot: ' + str(SelectedItemSlot) + 'b}]')
    if not Inventory == None:
        return str(Inventory['id'].replace('minecraft:', ''))
    return None
    
def get_player_pos(server, player):# get玩家坐标
    api = server.get_plugin_instance('PlayerInfoAPI')
    return api.getPlayerInfo(server, player, path='Pos')
    
def item_pos_change(item, pos_x, pos_y, pos_z):
    data_list = config_data()
    for i in range(len(data_list)):  #英文id匹配
        name = data_list[i]["name"]
        if item == name:
            data = data_list[i]
            del data_list[i]
            with open(ConfigFilePath, 'w' ,encoding='UTF-8') as yml:
                data['pos_x'] = pos_x
                data['pos_y'] = pos_y
                data['pos_z'] = pos_z
                data_list.append(data)
                yaml.safe_dump_all(data_list,yml,allow_unicode=True)
                yml.close()
                return
                   
                    
        
def on_info(server ,info):
    content = info.content
    command = content.split(' ')
    if len(command) == 0 or command[0] != Prefix:
        return
    del command[0]
    
    if len(command) == 0:
        server.tell(info.player,HelpMessage)
        return
    
    if len(command) in [1,2] and command[0] == 'search': #!!IS search <Item> 搜索
        try:
            item = command[1]
        except IndexError:
            item = get_item_name(server, info.player)
        if not item == None:
            name_search(server, item, info.player, True)
        else:
            server.tell(info.player,'[IS]你并未手持任何物品')
        
    elif len(command) in [3,4] and command[0] == 'add':#!!IS add <Item/hand> <Item_cn> [-f]添加物品模块
        api = server.get_plugin_instance('MinecraftItemAPI')
        force = False
        try:
            if command[3] == '-f':
                force = True
        except IndexError:
            force = False
        finally:
            if force == False:
                if command[1] == 'hand':
                    item = get_item_name(server, info.player)
                else:
                    item = command[1]
                if not api.getMinecraftItemInfo(item):
                    server.tell(info.player,'[IS] §e' + item + ' §r不是正确的MC物品ID')
                    return
                elif not name_search(server, item, info.player, False):
                    pos = get_player_pos(server, info.player)
                    pos_x = int(pos[0])
                    pos_y = int(pos[1])
                    pos_z = int(pos[2])
                    item_add(item, pos_x, pos_y, pos_z, command[2] ,server)
                    server.tell(info.player,'''
[IS]英文id: §e{},
§r[IS]中文id: §e{}
§r[IS]坐标:§b[x:{} , y:{}, z:{}]
§r[IS]已成功录入数据库'''.format(item,command[2],str(pos_x),str(pos_y),str(pos_z)))
                else:
                    server.tell(info.player,'[IS]已在列表中')
            elif force:
                if command[1] == 'hand':
                    item = get_item_name(server, info.player)
                else:
                    item = command[1]
                if official_name(item) == None:
                    pos = get_player_pos(server, info.player)
                    pos_x = int(pos[0])
                    pos_y = int(pos[1])
                    pos_z = int(pos[2])
                    item_add(item, pos_x, pos_y, pos_z, command[2] ,server)
                    server.tell(info.player,'''
[IS]英文id: §e{},
§r[IS]中文id: §e{}
§r[IS]坐标:§b[x:{} , y:{}, z:{}]
§r[IS]已成功录入数据库'''.format(item,command[2],str(pos_x),str(pos_y),str(pos_z)))
                else:
                    server.tell(info.player,'[IS]已在列表中')
            
    elif command[0] == 'override': #!!IS override <pos> <Item_name> 重写模块
        if command[1] == 'pos':
            try:
                item = command[2]
            except IndexError:
                item = get_item_name(server, info.player)
            if not item == None:
                if name_search(server, item, info.player, False):
                    pos = get_player_pos(server, info.player)
                    pos_x = int(pos[0])
                    pos_y = int(pos[1])
                    pos_z = int(pos[2])
                    item_pos_change(item, pos_x, pos_y, pos_z)
                    server.tell(info.player,'[IS] §e{} §r的坐标已被改写为§b[x:{} ,y:{} ,z:{}]'.format(item,str(pos_x),str(pos_y),str(pos_z)))
                else:
                    server.say('[IS]该物品数据无法找到，请确定你的输入没有错误')
            else:
                server.say('你手上没有物品')
        elif command[1] == 'nick' and len(command) in [4,5]:#!!IS override nick <add/remove/list> <Item_name/hand> <Nick>
            if command[2] == 'add':#添加nick / nick add <item_name/hand> <Nick>
                if command[3] == 'hand':#检测手中物品
                    item = get_item_name(server, info.player)
                    if not item == None:
                        try:
                            nick = command[4]
                        except IndexError:
                            server.tell(info.player,'[IS]你未输入常用名')
                            return
                        item_add_nickname(server, info.player, item, nick)
                    elif item == None:
                        server.tell(info.player,'[IS]你并未手持任何物品')
                        return
                else:
                    name = command[3]
                    item = official_name(name)
                    if not item == None:
                        try:
                            nick = command[4]
                        except IndexError:
                            server.tell(info.player,'[IS]你未输入你未输入常用名')
                            return
                        else:
                            item_add_nickname(server, info.player, item, nick)
                    else:
                        server.tell(info.player,'[IS]错误的物品id')
            elif command[2] == 'remove':#删除nick    item_del_nickname(server, player, item, nick_name)
                if command[3] == 'hand':#检测手中物品
                    item = get_item_name(server, info.player)
                    if not item == None:
                        try:
                            nick = command[4]
                        except IndexError:
                            server.tell(info.player,'[IS]你未输入你未输入常用名')
                            return
                        item_del_nickname(server, info.player, item, nick)
                    elif item == None:
                        server.tell(info.player,'[IS]你并未手持任何物品')
                        return
                else:
                    name = command[3]
                    item = official_name(name)
                    if not item == None:
                        try:
                            nick = command[4]
                        except IndexError:
                            server.tell(info.player,'[IS]你未输入你未输入常用名')
                            return
                        else:
                            item_del_nickname(server, info.player, item, nick)
                    else:
                        server.tell(info.player,'[IS]错误的物品id')
            elif command[2] == 'list':#列出nick   nickname_list(server, player, item)
                if command[3] == 'hand':#检测手中物品
                    item = get_item_name(server, info.player)
                    if not item == None:
                        nickname_list(server, info.player, item)
                    elif item == None:
                        server.tell(info.player,'[IS]你并未手持任何物品')
                        return
                else:
                    name = command[3]
                    item = official_name(name)
                    if not item == None:
                        nickname_list(server, info.player, item)
                    else:
                        server.tell(info.player,'[IS]错误的物品id')
        elif len(command) == 4 and command[1] == 'name_cn':#item_change_name_cn(server, player, item, name_cn)   !!IS override name_cn <item/hand> <name_cn>
            if command[2] == 'hand':
                item = get_item_name(server, info.player)
                if not item == None:
                    item_change_name_cn(server, info.player, item, command[3])
                else:
                    server.tell(info.player,'[IS]你并未手持任何物品')
            else:
                name = command[2]
                item = official_name(name)
                if not item == None:
                    item_change_name_cn(server, info.player, item, command[3])
                else:
                    server.tell(info.player,'[IS]未在数据库内读取到该ID')
    elif command[0] == 'data' and len(command) == 2: #print_item_data(server, player, item)  !!IS data <hand/item_name>
        if command[1] == 'hand':
            item = get_item_name(server, info.player)
            if not item == None:
                print_item_data(server, info.player, item)
            else:
                server.tell(info.player,'[IS]你并未手持任何物品')
        else:
            name = command[1]
            item = official_name(name)
            if not item == None:
                print_item_data(server, info.player, item)
            else:
                server.tell(info.player,'[IS]未在数据库内读取到该ID')
            