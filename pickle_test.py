import pickle

merchingList = []

#merchingList.append((["Torva full helm (damaged)", "bandosComponents"], [1, "bandosComponentsQuantity"], "Torva full helm", 1))
#merchingList.append((["Torva platebody (damaged)", "bandosComponents"], [1, "2*bandosComponentsQuantity"], "Torva platebody", 1))
#merchingList.append((["Torva platelegs (damaged)", "bandosComponents"], [1, "2*bandosComponentsQuantity"], "Torva platelegs", 1))

#merchingList.append((["Masori mask", "armadylPlates"], [1, "armadylPlatesQuantity"], "Masori mask (f)", 1))
#merchingList.append((["Masori body", "armadylPlates"], [1, "4*armadylPlatesQuantity"], "Masori body (f)", 1))
#merchingList.append((["Masori chaps", "armadylPlates"], [1, "3*armadylPlatesQuantity"], "Masori chaps (f)", 1))

merchingList.append((["Masori mask (f)", "Masori chaps (f)", "Masori body (f)"], [1,1,1], "Masori armour set (f)", 1))
merchingList.append((["Inquisitor's plateskirt", "Inquisitor's hauberk", "Inquisitor's great helm"], [1,1,1], "Inquisitor's armour set", 1))
merchingList.append((["Ancestral hat", "Ancestral robe top", "Ancestral robe bottom"],[1,1,1],"Ancestral robes set",1))
merchingList.append((["Justiciar faceguard", "Justiciar chestguard", "Justiciar legguards"],[1,1,1],"Justiciar armour set",1))

#merchingList.append(([["Bow of faerdhinen (inactive)","Blade of saeldor (inactive)"], "crystalShards"],[[1,1], "250*crystalShardsQuantity"],"Enhanced crystal weapon seed",1))
#merchingList.append((["Enhanced crystal weapon seed", "crystalShards"],[1, "100*crystalShardsQuantity"],"Bow of faerdhinen (inactive)",1))
merchingList.append((["Armadyl crossbow", "Nihil horn", "Nihil shard"], [1,1,250], "Zaryte crossbow", 1))
merchingList.append(("Venator shard", 5, "Venator bow (uncharged)", 1))
merchingList.append((["Voidwaker blade", "Voidwaker hilt", "Voidwaker gem"],[1,1,1],"Voidwaker",1,500000))

merchingList.append((["Zamorakian spear"],[1],"Zamorakian hasta",1,150000))
merchingList.append((["Zamorakian hasta", "Hydra's claw"],[1,1],"Dragon hunter lance",1))
merchingList.append((["Kodai insignia", "Master wand"],[1,1],"Kodai wand",1))
merchingList.append((["Imbued heart", "Ancient essence"],[1,150000],"Saturated heart",1))

merchingList.append(([["Thammaron's sceptre (u)","Thammaron's sceptre (au)"], "Skull of vet'ion"],[[1,1],1],[["Accursed sceptre (u)","Accursed sceptre (au)"]],[[1,1]]))
merchingList.append((["Craw's bow (u)", "Fangs of venenatis"],[1,1],"Webweaver bow (u)",1))
merchingList.append((["Viggora's chainmace (u)", "Claws of callisto"],[1,1],"Ursine chainmace (u)",1))

merchingList.append((["Spirit shield", "Holy elixir"],[1,1],"Blessed spirit shield",1))
merchingList.append((["Elysian sigil", "Blessed spirit shield"],[1,1],"Elysian spirit shield",1))

merchingList.append((["Spectral sigil", "Blessed spirit shield"],[1,1],"Spectral spirit shield",1))
merchingList.append((["Odium shard 1", "Odium shard 2", "Odium shard 3"],[1,1,1],"Odium ward",1))
merchingList.append((["Malediction shard 1", "Malediction shard 2", "Malediction shard 3"],[1,1,1],"Malediction ward",1))

merchingList.append((["Draconic visage", "Anti-dragon shield"],[1,1],"Dragonfire shield",1))
merchingList.append((["Skeletal visage", "Anti-dragon shield"],[1,1],"Dragonfire ward",1))
merchingList.append((["Wyvern visage", "Elemental shield"],[1,1],"Ancient wyvern shield",1))

merchingList.append((["Eternal crystal", "Infinity boots"],[1,1],"Eternal boots",1))
merchingList.append((["Pegasian crystal", "Ranger boots"],[1,1],"Pegasian boots",1))
merchingList.append((["Primordial crystal", "Dragon boots"],[1,1],"Primordial boots",1))

merchingList.append((["Zenyte shard", ["Uncut onyx", "Onyx"], "Cosmic rune", "Soul rune", "Blood rune", "Gold bar"], [1, [1,1], 1, 20, 20, 1], [["Necklace of anguish", "Amulet of torture", "Tormented bracelet", "Ring of suffering"]], [[1,1,1,1]]))

with open('MerchingList.pkl', 'wb') as f:
    pickle.dump(merchingList, f)

with open('MerchingList.pkl', 'rb') as f:
    merchingList = pickle.load(f)

for x in merchingList:
    print(x)