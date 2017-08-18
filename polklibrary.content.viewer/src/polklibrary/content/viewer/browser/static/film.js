var ShowMore = {
        
    Pattern : function() {
        $('.pat-showmore').each(function(i,t) {
            ShowMore.Attach(t);
        });
    },
    
   
    Attach : function(e) {
        var element = e;
        var i = parseInt($(element).attr('data-len'));
        var text = $(element).text();
        var show = $('<span>').html( text.substring(0, i) ).addClass("showmore-show");
        var hide = $('<span>').html( text.substring(i, text.length) ).addClass("showmore");
        var toggle = $('<span>').html('...  Show More').addClass("showmore-toggle").click(function(){
            $(this).parent().find('.showmore').show();
            $(this).hide();
        });
        
        $(element).html(""); // destroy text
        $(element).append(show).append(toggle).append(hide);
    }
    
}


var Scroll = {

    ImageSpace : 210, // 200px record image + 10px margin

    Pattern : function() {
        $('.pat-scroll .collection').hover(
            function(){
                $(this).find('.scroll-left,.scroll-right').show();
            },
            function(){
                $(this).find('.scroll-left,.scroll-right').hide();
            }
        );
        
        // Tap or Mouse
        $('.pat-scroll .scroll-right').click(function(){
            Scroll.GoRight(this);
        });
        $('.pat-scroll .scroll-left').click(function(){
            Scroll.GoLeft(this);
        });
        
        // Swipes
        $('.pat-scroll .scrollbox').swipe(function(event, direction, distance, duration, fingerCount, fingerData){
            if (direction == 'left')
                Scroll.GoLeft(this);
            else
                Scroll.GoRight(this);
            
        });
        // $('.pat-scroll .scrollbox').swipe(function(){
            // Scroll.GoRight(this);
        // });
        
    },
    
    GetScrollDistance : function(){
        var scroll_distance = $('.collection').width();
        var distance = 0;
        
        if (this.ImageSpace >= scroll_distance)
            distance = this.ImageSpace;
        else if (this.ImageSpace*2 >= scroll_distance)
            distance =  this.ImageSpace*2;
        else if (this.ImageSpace*3 >= scroll_distance)
            distance =  this.ImageSpace*3;
        else if (this.ImageSpace*4 >= scroll_distance)
            distance =  this.ImageSpace*4;
        else if (this.ImageSpace*5 >= scroll_distance)
            distance =  this.ImageSpace*5;
        else if (this.ImageSpace*6 >= scroll_distance)
            distance =  this.ImageSpace*6;
        else if (this.ImageSpace*7 >= scroll_distance)
            distance =  this.ImageSpace*7;
        else if (this.ImageSpace*8 >= scroll_distance)
            distance =  this.ImageSpace*8;
        else
            distance =  this.ImageSpace*9;
            
        return distance - this.ImageSpace; // back up one
        
    },
    
    
    GoRight : function(element){
        var scrollbox = $(element).parent().find('.scrollbox');
        var left = parseInt($(scrollbox).css('left').replace('px',''));
        var max_distance = (parseInt($(scrollbox).attr('data-items')) * Scroll.ImageSpace) + Scroll.ImageSpace; // +  "View More"
        var scroll_distance = Scroll.GetScrollDistance();
        
        if (-max_distance < left-scroll_distance)
            $(scrollbox).css({'left': (left - scroll_distance) + "px"});
    },
    
    GoLeft : function(element){
        var scrollbox = $(element).parent().find('.scrollbox');
        var left = parseInt($(scrollbox).css('left').replace('px',''));
        var scroll_distance = Scroll.GetScrollDistance();

        if (left+scroll_distance <= 0) 
            $(scrollbox).css({'left': (left + scroll_distance) + "px"});
    },

    
    
    
}



var Overlay = {
    
    Thread: null,
    Width: 400,
    PushLeft: 200,
    PushRight: 425,
    
    Pattern : function(){
        
        $('.pat-overlay').hover(
            function(e){
                clearTimeout(Overlay.Thread);
                //var element = this;
            
                var position = $(this).offset();
                var window_width = $(window).width();
                var left = position.left + Overlay.PushLeft;
                var top = position.top;
                
                if ((left + Overlay.Width) < window_width){
                    $('#overlay').css({'left': left, 'top': position.top});
                    $('#overlay').addClass('rightside');
                    $('#overlay').removeClass('leftside');
                }
                else {
                    var right = position.left - Overlay.PushRight;
                    $('#overlay').css({'left': right, 'top': position.top});
                    $('#overlay').addClass('leftside');
                    $('#overlay').removeClass('rightside');
                }
                Overlay.Set(this);                
                Overlay.Show();
            },
            function(){                
                Overlay.Thread = setTimeout(function(){
                        Overlay.Clear();
                        Overlay.Hide();
                }, 500);
            }
        );
        
        $('#overlay').hover(
            function(e){
                clearTimeout(Overlay.Thread);
            },
            function(){
                Overlay.Clear();
                Overlay.Hide();
            }
        );
        
        
        
    },

    Set : function(element){
        $('#overlay').find('.title').html($(element).attr('data-overlay-title'));
        $('#overlay').find('.description').html($(element).attr('data-overlay-description'));
        ShowMore.Attach($('#overlay').find('.description'));
        
        $('#overlay').find('.runtime span').html($(element).attr('data-overlay-runtime'));
        
        var span = $(element).find('.add-to-list span').clone(true, true);
        $(span).removeClass('suppress-add-to-list');
        Films.Attach(span);
        if (span != null && span.length > 0)
            $('#overlay').find('.add-to-list span').replaceWith(span);
    },
    
    Clear : function(element){
        $('#overlay').find('.title').html('');
        $('#overlay').find('.description').html('');
        $('#overlay').find('.runtime span').html('');
    },
    
    Show : function(){
        $('#overlay').css({'opacity':'1','visibility': 'visible'});
    },
    
    Hide : function(){
        $('#overlay').css({'opacity':'0','visibility': 'hidden'});
    },
    
}


var Share = {

    Pattern : function() {
        $('.pat-share').click(function(){
            $('#share').css({'opacity':'1','visibility': 'visible'});
            var url = $('body').attr('data-base-url');
            var embed = '<iframe width="600px" height="420px" frameborder="0" scrolling="no" src="' + url + '/share"></iframe>';
            $('#share textarea').text(embed);
            
            
        });
        $('#share .close').click(function(){
            $('#share').css({'opacity':'0','visibility': 'hidden'});
        });
    },

}










var Films = {
    
    Items : {},
    
    Pattern : function(){
        
        $('span.pat-film-list').each(function(i, t){
            // Set if has or does not
            if (Films.Items.hasOwnProperty($(t).attr('data-id'))) {
                $(t).attr('data-added', '1').attr('title', 'Remove from your playlist');
            }
            else {
                $(t).attr('data-added', '0').attr('title', 'Add to your playlist');
            }
            
            // Add Clicks
            Films.Attach(t);
            
        });
        
    },
    
    Attach : function(element){
        $(element).click(function(e){
            e.preventDefault();
            if ($(e.target).attr('data-added') == '1') {
                Films.Remove($(e.target).attr('data-id'), function(response){
                    if(response.status == 200)
                        $(element).attr('data-added', '0').attr('title', 'Add to your playlist');
                });
            }
            else {
                Films.Add($(e.target).attr('data-id'), function(response){
                    if(response.status == 200)
                        $(element).attr('data-added', '1').attr('title', 'Remove from your playlist');
                });
            }
            
        });
    },
        
    Get : function(callback) {
        $.getJSON($('body').attr('data-portal-url') + '/setFilm', function(response){
            if (response.status == 200) {
                var items = response.data.split('|');
                for(var i in items)
                    if (items[i] != '')
                        Films.Items[items[i]] = items[i];
                callback();
             }
             else {
                callback();
             }
        });
    },
    
    Add : function(id, callback){
        $.getJSON($('body').attr('data-portal-url') + '/setFilm?type=add&id=' + id, function(response){
            console.log(response);
            callback(response);
        });
    },

    Remove : function(id, callback){
        $.getJSON($('body').attr('data-portal-url') + '/setFilm?type=remove&id=' + id, function(response){
            console.log(response);
            callback(response);
        });
    },

}


$(document).ready(function(){
    Films.Get(function(response){
        Films.Pattern();
    });
    Scroll.Pattern();
    Overlay.Pattern();
    ShowMore.Pattern();
    Share.Pattern();
});

