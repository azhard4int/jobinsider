__author__ = 'azhar'
for ab in range(73, 80):
    print """INSERT INTO `saasvtr`.`users_modules` (`id`, `mods_id`, `user_id`) VALUES (NULL, '1', '{0}');""".format(ab)