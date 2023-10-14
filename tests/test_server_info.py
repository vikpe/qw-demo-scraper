import context

context.apply()

from vendor import server_info


def describe_from_string():
    def test_all_values():
        info_str = r"\maxfps\77\pm_ktjump\1\*version\MVDSV 0.36\*z_ext\511\maxspectators\12\*admin\lolek <lolek@quake1.pl>\ktxver\1.42\sv_antilag\2\needpass\4\*gamedir\qw\timelimit\10\deathmatch\3\teamplay\2\mode\2on2\*qvm\so\*progs\so\maxclients\4\map\dm4"

        assert server_info.ServerInfo.from_string(info_str) == server_info.ServerInfo(
            admin="lolek <lolek@quake1.pl>",
            deathmatch=3,
            gamedir="qw",
            ktxver="1.42",
            map="dm4",
            maxclients=4,
            maxfps=77,
            maxspectators=12,
            mode="2on2",
            needpass=4,
            pm_ktjump=1,
            progs="so",
            qvm="so",
            sv_antilag=2,
            teamplay=2,
            timelimit=10,
            version="MVDSV 0.36",
            z_ext="511",
        )

    def test_few_values():
        info_str = r"\maxfps\77\pm_ktjump\1"

        assert server_info.ServerInfo.from_string(info_str) == server_info.ServerInfo(
            maxfps=77,
            pm_ktjump=1,
            gamedir=None,
        )
