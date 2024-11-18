import os
import subprocess

import psutil
from keys import keys

from libqtile import hook

from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

# Colors

colorBarra = "#1b004b"
tamañoBarra = 30

fuentePredeterminada = "ProFont IIx Nerd Font"
tamañoFuente = 12

grupoTamañoIcon = 22
grupoTamañoFuente = 20
grupoForeGround = "#f988ff"

grupoColorActivo = "#bc4ed8"
grupoColorInactivo = "#4c007d"

grupoThisCurrentScreenBorder = "#7f00b2"
grupoThisScreenBorder = "#cd581f"
grupoUrgentBorderColor = "#1f8fcd"

windowNameForeground = "#bd93f9"
windowNameBackground = "#1b004b"

colorHaveUpdates = "#bc0000"
dispositivoRed1 = "eno1"
dispositivoRed2 = "wlan0"

colorGrupoInfo0 = "#81638b"
colorGrupoInfoFont0 = "#ffffff"

colorGrupoInfo1 = "#69dde4"
colorGrupoInfoFont1 = "#327847"

colorGrupoInfo2 = "#f26dc9"
colorGrupoInfoFont2 = "#e0b0ff"

colorGrupoInfo3 = "#e0b0ff"
colorGrupoInfoFont3 = "#614051"

colorGrupoInfo4 = "#fe4e74"
colorGrupoInfoFont4 = "#9d98cd"

def separador(tamañoPadding):
    return widget.Sep(
                    linewidth = 0,
                    padding = tamañoPadding,
                    foreground = grupoForeGround,
                    background = colorBarra
                )

def circle(setType, color):
    return widget.TextBox(
                    text = ("" if (setType==0) else ""),
                    fontsize = grupoTamañoFuente + 3,
                    foreground = color,
                    background = colorBarra,
                    padding = -1
                )

def grupoInfo(icon, color_grupo, color_font):
    return widget.TextBox(
                    text = icon,
                    fontsize = tamañoFuente,
                    foreground = color_font,
                    background = color_grupo
                )

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in [
        "", "󰒍", "", "󰎆", " "
    ]]

for i, group in enumerate(groups):
    numeroEscrito =str(i+1)
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                numeroEscrito,
                lazy.group[group.name].toscreen(),
                desc=f"Switch to group {group.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                numeroEscrito,
                lazy.window.togroup(group.name, switch_group=True),
                desc=f"Switch to & move focused window to group {group.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=2, margin=18),
    layout.Max(),
    layout.TreeTab(),
]

widget_defaults = dict(
    font=fuentePredeterminada,
    fontsize=tamañoFuente,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    active = grupoColorActivo,
                    fontsize = grupoTamañoIcon,
                    disable_drag = True,
                    border_width = 1,
                    foreground = grupoForeGround,
                    highlight_method = 'block',
                    inactive = grupoColorInactivo,
                    margin_x = 0,
                    margin_y = 5,
                    padding_x = 15,
                    padding_y = 10,
                    other_current_screen_border = grupoThisScreenBorder,
                    other_screen_border = grupoThisCurrentScreenBorder,
                    this_current_screen_border = grupoThisCurrentScreenBorder,
                    this_screen_border = grupoThisScreenBorder,
                    urgent_alert_method = 'block',
                    urgent_border = grupoUrgentBorderColor
                ),
                separador(20),
                widget.Prompt(),
                widget.WindowName(
                    foreground=windowNameForeground,
                    background = windowNameBackground
                ),
                widget.Systray(
                    icon_size = grupoTamañoFuente,
                    background = colorBarra
                ),
                separador(10),
                #GRUPO INFO 0
                circle(0, colorGrupoInfo0),
                widget.BatteryIcon(
                    background = colorGrupoInfo0,
                    scale= 1.2,
                ),
                widget.Battery(
                    background = colorGrupoInfo0,
                    foreground = colorGrupoInfoFont0,
                    format='{percent:2.0%}',
                    update_interval= 1,
                ),
                circle(1, colorGrupoInfo0),

                #GRUPO INFO 1
                circle(0, colorGrupoInfo1),
                grupoInfo(" ", colorGrupoInfo1, colorGrupoInfoFont1),
                widget.ThermalSensor(
                    background = colorGrupoInfo1,
                    foreground = colorGrupoInfoFont1,
                    format='{temp:.1f}°C',
                    update_interval=1,
                    threshold=65.0,
                    sensor='k10temp-pci-00c3',
                ),
                grupoInfo(" ", colorGrupoInfo1, colorGrupoInfoFont1),
                widget.Memory(
                    background = colorGrupoInfo1,
                    foreground = colorGrupoInfoFont1
                ),
                circle(1, colorGrupoInfo1),
                
                #GRUPO INFO 2
                circle(0, colorGrupoInfo2),
                grupoInfo("󰁪", colorGrupoInfo2, colorGrupoInfoFont2),
                widget.CheckUpdates(
                    background = colorGrupoInfo2,
                    colour_have_updates = colorHaveUpdates,
                    colour_no_updates = colorGrupoInfoFont2,
                    no_update_string = '0',
                    display_format = '{updates}',
                    update_interval = 1800,
                    distro="Arch_checkupdates"
                ),
                grupoInfo(" 󰓅", colorGrupoInfo2, colorGrupoInfoFont2),
                widget.Net(
                    foreground = colorGrupoInfoFont2,
                    background = colorGrupoInfo2,
                    format = '{down:>8.2f} {up:>8.2f}', 
                ),
                circle(1, colorGrupoInfo2),

                #GRUPO INFO 3
                circle(0, colorGrupoInfo3),
                widget.Clock(
                    format="%a %d/%m/%Y %I:%M %p",
                    background = colorGrupoInfo3,
                    foreground = colorGrupoInfoFont3
                ),
                grupoInfo(" ", colorGrupoInfo3, colorGrupoInfoFont3),
                widget.PulseVolume(
                    background = colorGrupoInfo3,
                    foreground = colorGrupoInfoFont3,
                    limit_max_volume = True,
                    fontsize = tamañoFuente
                ),
                circle(1, colorGrupoInfo3),

                #GRUPO INFO 4
                circle(0, colorGrupoInfo4),
                widget.CurrentLayoutIcon(
                    background = colorGrupoInfo4,
                    foreground = colorGrupoInfoFont4,
                    scale = 0.7
                ),
                widget.CurrentLayout(
                    background = colorGrupoInfo4,
                    foreground = colorGrupoInfoFont4
                ),
                circle(1, colorGrupoInfo4)
            ],
            tamañoBarra,
            background=colorBarra,
            opacity = 0.85,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([script]) 
