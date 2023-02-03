function convert(rgb) {
    if (/^#[0-9A-F]{6}$/i.test(rgb)) return rgb;
    rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
    function hexCode(i) {
        return ("0" + parseInt(i).toString(16)).slice(-2);
    }
    return "#" + hexCode(rgb[1]) + hexCode(rgb[2])
            + hexCode(rgb[3]);
}

document.querySelector("#darkmode-button").onclick = function(e){
darkmode.toggleDarkMode();
$('.special_option').css('background-color', convert($('body').css("background-color")));
$('.special_option').prop('value', convert($('body').css("background-color")));
if (convert($('body').css("background-color")) == "#ffffff") {
$('.palette').css('background-image', "url({% static 'palette-light.svg' %})");
}
else {
$('.palette').css('background-image', "url({% static 'palette-dark.svg' %})");
}
}

setTimeout(() => {
$('.special_option').css('background-color', convert($('body').css("background-color")));
$('.special_option').prop('value', convert($('body').css("background-color")));
if (convert($('body').css("background-color")) == "#ffffff") {
$('.palette').css('background-image', "url({% static 'palette-light.svg' %})");
}
else {
$('.palette').css('background-image', "url({% static 'palette-dark.svg' %})");
}
}, 300);