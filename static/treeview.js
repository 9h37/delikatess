function filltable (li)
{
    var div = li.getElementsByTagName ('div')[0];
    var children = div.children[0].children;

    $("#table").empty ();

    for (var i = 0, c = children.length; i < c; i++)
    {
        var a = children[i].getElementsByTagName ('a')[0];
        var cdiv = children[i].getElementsByTagName ('div')[0];

        var img = $('<img/>');
        img.attr ({
            alt: "",
            src: (cdiv.hasChildNodes () ? "/static/images/folder-closed.gif" : "/static/images/file.gif")
        });

        // create elements for the table
        var tr = $('<tr/>');

        // name
        var td = $('<td/>');
        td.append (img);

        if (cdiv.hasChildNodes ())
        {
            var link = $('<a/>');

            link.attr ({
                href: "#",
                title: a.title
            });
            link.text (a.innerHTML);
            link.PARENT = a.parentNode;
            link.click (function () {
                toggle (link.PARENT, true);
            });
            td.append (link);
        }
        else
            td.append (a.innerHTML);

        tr.append (td);

        // size
        td = $('<td/>');
        td.text ("unknow");
        tr.append (td);

        // date
        td = $('<td/>');
        td.text ("0");
        tr.append (td);

        // actions
        td = $('<td/>');
        td.text ("X");
        td.a = a;
        tr.append (td);

        $("#table").append (tr);
    }
}

// Integrate treeview with the topbar
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
        go (name, li);
        filltable (li);
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

// toggle visiblity of children in the treeview
function toggle (el, alwaysShow)
{
    var children = el.getElementsByTagName ('div')[0];

    // if there is no child in the children's div,
    // there is anything to do.
    if (children.hasChildNodes () == false)
        return;


    $('#nav').empty ();

    // if children are hidden, show them
    if (alwaysShow == true || children.style.display == "none" || children.style.display == "")
    {
        children.style.display = "block";
        el.style.backgroundImage = "url('/static/images/folder.gif')"

        // go to the current level
        go (el.getElementsByTagName ('a')[0].innerHTML, el);

        // now fill the table
        filltable (el);
    }
    else // if they are visible, hide them
    {
        children.style.display = "none";
        el.style.backgroundImage = "url('/static/images/folder-closed.gif')"

        // go to the parent level
        var li = el.parentNode.parentNode.parentNode;
        if (li.tagName == "LI")
        {
            go (li.getElementsByTagName ('a')[0].innerHTML, li);

            // now fill the table
            filltable (li);
        }
    }

}

// Remove files from the treeview
function render ()
{
    var divs = $('.children');

    for (var i = 0, c = divs.length; i < c; i++)
    {
        var children = divs[i];
        if (children.hasChildNodes () == false)
        {
            li = children.parentNode;
            li.style.display = "none";
        }
    }
}

