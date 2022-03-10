// if ( window.history.replaceState ) {
//     window.history.replaceState( null, null, window.location.href );
// }

// function closeModal() {
//     document.querySelector('.modal').style.display = 'none'
// }

// function handleModal() {
//     document.querySelector('.modal').style.display = 'flex'
//     let authForm = document.getElementsByClassName('auth-form__form')
//     for ( let i = 0; i < authForm.length; i++) {
//         authForm[i].classList.remove('auth-active')
//     }
// }

// function loginPage() {
//     handleModal()
//     document.getElementById('login').classList.add('auth-active')
// }

// function registerPage() {
//     handleModal()
//     document.getElementById('register').classList.add('auth-active')
    
// }

// function Pageregister() {
//     handleModal()
//     document.getElementById('register').classList.add('auth-active')
// }

// function handleLogin() {
//     document.getElementById('form-login').addEventListener('submit', function() {
//         console.log('ok')
//     })
// }

const updateBtns = document.getElementsByClassName('update-cart')
console.log(updateBtns)
const lengthUpdateBtns = updateBtns.length
for (let i = 0; i < lengthUpdateBtns; i++) {
    updateBtns[i].addEventListener('click', function(){
        const productId = this.dataset.product
        try {
            var productColor = document.getElementsByClassName('option-active')[1].dataset.color
        } catch {
            var productColor = this.dataset.color
        }
        const action = this.dataset.act
        if (user === 'AnonymousUser'){
            addCookieItem(productId, productColor, action)
        } else {
            delete_cookie('cart')
            updateUserCart(productId, productColor, action)
        }
    })
}

// =================== USER AUTHENTICATED ADD TO CARD ======================
function updateUserCart(productId, productColor, action) {
    console.log(productId, productColor, action)
    url = 'http://127.0.0.1:8000/gio-hang/update-cart/'
    fetch(url, {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'productColor': productColor,
            'action': action,
        })
    })
    .then((response) => response.json())
    .then(() => location.reload())

}

// ===================== ANONYMOUS USER ADD TO CART ======================== 
function addCookieItem(productId, productColor, action) {
    if (action == 'add') {
        var key = 1
        var product = productId + '_' + productColor
        if (cart[product] == undefined) {
            cart[product] = {'productId': productId, 'productColor': productColor, 'quantity': 1}
        }else {
            if (cart[product]['productId'] == productId && cart[product]['productColor'] == productColor ) {
                cart[product]['quantity'] += 1
            } else {
                key += 1
                var product = productId + '_' + productColor
                cart[product] = {'productId': productId, 'productColor': productColor, 'quantity': 1}
            }
        }
    }
    if (action == 'remove') {
        var product = productId + '_' + productColor
        cart[product]['quantity'] -= 1
        if (cart[product]['quantity'] <= 0) {
            delete cart[product]
        }
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    window.location.reload()
}


var delete_cookie = function(name) {
    document.cookie = 'cart=' + ";domain=;path=/;expires=Thu, 01 Jan 1970 00:00:00 GMT"
};


function humanized_time_span(date, ref_date, date_formats, time_units) {
    //Date Formats must be be ordered smallest -> largest and must end in a format with ceiling of null
    date_formats = date_formats || {
      past: [
        { ceiling: 60, text: "just now"},
        { ceiling: 3600, text: "$minutes minutes ago" },
        { ceiling: 86400, text: "$hours hours ago" },
        { ceiling: 2629744, text: "$days days ago" },
        { ceiling: 31556926, text: "$months months ago" },
        { ceiling: null, text: "$years years ago" }      
      ],
      future: [
        { ceiling: 60, text: "in $seconds seconds" },
        { ceiling: 3600, text: "in $minutes minutes" },
        { ceiling: 86400, text: "in $hours hours" },
        { ceiling: 2629744, text: "in $days days" },
        { ceiling: 31556926, text: "in $months months" },
        { ceiling: null, text: "in $years years" }
      ]
    };
    //Time units must be be ordered largest -> smallest
    time_units = time_units || [
      [31556926, 'years'],
      [2629744, 'months'],
      [86400, 'days'],
      [3600, 'hours'],
      [60, 'minutes'],
      [1, 'seconds']
    ];
    
    date = new Date(date);
    ref_date = ref_date ? new Date(ref_date) : new Date();
    var seconds_difference = (ref_date - date) / 1000;
    
    var tense = 'past';
    if (seconds_difference < 0) {
      tense = 'future';
      seconds_difference = 0-seconds_difference;
    }
    
    function get_format() {
      for (var i=0; i<date_formats[tense].length; i++) {
        if (date_formats[tense][i].ceiling == null || seconds_difference <= date_formats[tense][i].ceiling) {
          return date_formats[tense][i];
        }
      }
      return null;
    }
    
    function get_time_breakdown() {
      var seconds = seconds_difference;
      var breakdown = {};
      for(var i=0; i<time_units.length; i++) {
        var occurences_of_unit = Math.floor(seconds / time_units[i][0]);
        seconds = seconds - (time_units[i][0] * occurences_of_unit);
        breakdown[time_units[i][1]] = occurences_of_unit;
      }
      return breakdown;
    }
  
    function render_date(date_format) {
      var breakdown = get_time_breakdown();
      var time_ago_text = date_format.text.replace(/\$(\w+)/g, function() {
        return breakdown[arguments[1]];
      });
      return depluralize_time_ago_text(time_ago_text, breakdown);
    }
    
    function depluralize_time_ago_text(time_ago_text, breakdown) {
      for(var i in breakdown) {
        if (breakdown[i] == 1) {
          var regexp = new RegExp("\\b"+i+"\\b");
          time_ago_text = time_ago_text.replace(regexp, function() {
            return arguments[0].replace(/s\b/g, '');
          });
        }
      }
      return time_ago_text;
    }
            
    return render_date(get_format());
}