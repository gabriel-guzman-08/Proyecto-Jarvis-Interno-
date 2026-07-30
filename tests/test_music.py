from automation.chrome_remote import (
    get_tab
)

tab = get_tab()

tab.Page.navigate(
    url="https://music.youtube.com/watch?v=hTWKbfoikeg"
)