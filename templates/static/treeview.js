function go (name, li)
{
    var nli = $('<li/>');

    var nlink = $('<a/>');
    nlink.text (name);
    nlink.attr ("href", "#");

    // if the user click on a link in the topbar
    // go to this link.
    nlink.click (function () {
        $('#nav').empty ();
        go (name,li);
    });

    nli.append (nlink);
    $('#nav').prepend (nli);

    // Does the current level has a parent ?
    var div = li.parentNode.parentNode;
    if (div.tagName == "DIV" && div.className == "children")
    {
        var a = div.parentNode.getElementsByTagName ('a')[0];

        // if yes, add parents to the topbar
        go (a.innerHTML, div.parentNode);
        nli.prev ().attr ("class", "");
    }

    // set the last link as 'active'
    nli.attr ("class", "active");
}

function toggle (el)
{
    var children = el.getElementsByTagName ('div')[0];

    // if there is no child in the children's div,
    // there is anything to do.
    if (children.hasChildNodes () == false)
        return;

    $('#nav').empty ();

    // if children are hidden, show them
    if (children.style.display == "none" || children.style.display == "")
    {
        children.style.display = "block";
        el.style.backgroundImage = "url('/static/images/folder.gif')"

        // go to the current level
        go (el.getElementsByTagName ('a')[0].innerHTML, el);
    }
    else // if they are visible, hide them
    {
        children.style.display = "none";
        el.style.backgroundImage = "url('/static/images/folder-closed.gif')"

        // go to the parent level
        var li = el.parentNode.parentNode.parentNode;
        if (li.tagName == "LI")
            go (li.getElementsByTagName ('a')[0].innerHTML, li);
    }
}

function render ()
{
    var divs = $('.children');

    for (var i = 0, c = divs.length; i < c; i++)
    {
        var children = divs[i];
        if (children.hasChildNodes () == false)
        {
            li = children.parentNode;
            li.style.backgroundImage = "url('/static/images/file.gif')";
        }
    }
}

