document.addEventListener('DOMContentLoaded', () => {
    // navigation bar
    const nav_bar = document.getElementById('nav_bar');
    let last_scroll = 0;

    window.addEventListener('scroll', () => {
        const current_scroll = window.pageYOffset

        if (current_scroll <= 0) {
            nav_bar.classList.remove('drop-shadow-md');
        }

        if (current_scroll > last_scroll && !nav_bar.classList.contains('-translate-y-full')) {
            nav_bar.classList.remove('drop-shadown-md');
            nav_bar.classList.add('-translate-y-full');
        }

        if (current_scroll < last_scroll && nav_bar.classList.contains('-translate-y-full')) {
            nav_bar.classList.remove('-translate-y-full');
            nav_bar.classList.add('drop-shadow-md')
        }

        last_scroll = current_scroll
    })

    // notification drop box
    var notification_switch = document.getElementById('notification_switch');
    var notification_box = document.getElementById('notification_box');
    notification_switch.addEventListener('click', () => {
        if (notification_box.classList.contains('h-0')) {
            notification_box.classList.remove('h-0');
            notification_box.classList.add('h-5/6');
        } else if (notification_box.classList.contains('h-5/6')) {
            notification_box.classList.remove('h-5/6');
            notification_box.classList.add('h-0');    
        }
        })

    window.onclick = function (event) {
        var main_switch = event.target.matches('#notification_switch');
        var switch_one = event.target.matches('#switch_one');
        var switch_two = event.target.matches('#switch_two');
        var switch_three = event.target.matches('#switch_three');
        var switch_four = event.target.matches('#switch_four');
        var switch_five = event.target.matches('#switch_five');
            
        if (!main_switch && !switch_one && !switch_two && !switch_three && !switch_four && !switch_five) {   
            if (notification_box.classList.contains('h-5/6')) {
                notification_box.classList.remove('h-5/6');
                notification_box.classList.add('h-0');
            }
        }
    }

    // logout drop box
    const logout_switch_main = document.getElementById('logout_switch_main');
    const logout_box = document.getElementById('logout_box')
    logout_switch_main.addEventListener('mouseover', () => {
        logout_box.classList.remove('hidden');
    })

    window.addEventListener('click', (event) => {
        var logout_main = event.target.matches('#logout_switch_main');
        var logout_one = event.target.matches('#logout_switch_one');
        var logout_two = event.target.matches('#logout_switch_two');
        if (!logout_box.classList.contains('hidden') && !logout_main && !logout_one && !logout_two) {
            logout_box.classList.add('hidden');
        }
    })

    // profile edit box
    const profile_box_1 = document.querySelector('#profile_box_1')
    const profile_box_2 = document.querySelector('#profile_box_2');
    const profile_open_switch = document.querySelector('#profile_open_switch');
    const profile_close_switch = document.querySelector('#profile_close_switch');
    
    if (profile_open_switch) {
        profile_open_switch.addEventListener('click', () => {
            profile_box_1.classList.add('hidden');
            profile_box_2.classList.remove('hidden');
        })
    }
    
    if (profile_close_switch) {
        profile_close_switch.addEventListener('click', () => {
            profile_box_2.classList.add('hidden');
            profile_box_1.classList.remove('hidden');
        })
    }
})