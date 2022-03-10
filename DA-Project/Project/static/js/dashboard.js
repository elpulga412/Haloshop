function buildDashboard(){
  urlSearch()
  var contentTable = document.querySelector(".content-table")
  const urlSearchParams = new URLSearchParams(window.location.search);
  const params = Object.fromEntries(urlSearchParams.entries());
  var url = ""
  if (params.search != "undefined"){
    url = `/api/orders/?search=${params.search}`
    if (typeof(params.search) === "undefined"){
      url = `/api/orders/`
    }
  }
  fetch(url)
  .then(res => res.json())
  .then(function(data){
    if (window.location.href == "http://127.0.0.1:8000/dashboard/") {
      var orders = data.filter(function(orders){
        return (orders.status=="Pending" || orders.status=="Accepted")
      })
    } else{
        var orders = data
    }

    var arrayList = []
    contentTable.innerHTML = ""
    orders.forEach(function(order){
      arrayList.push(order)
      var btnPrint = ``
      if (order.status === "Completed"){
        btnPrint = `<i class="fa-solid fa-print"></i>`
      }
      content = ` <tr class="table-${order.id}">
                    <td class="dashboard-transaction">
                      <a data-bs-toggle="modal" data-bs-target="#exampleModal">${order.transaction_id}<a>
                    </td>
                    <td><a href="">${order.customer.email}<a></td>
                    <td>${order.full_name}</td>
                    <td>${order.phone}</td>
                    <td>${order.address}</td>
                    <td>${order.state}</td>
                    <td>${order.city}</td>
                    <td>
                      <select name="status" class="mySelect">
                        <option value="Pending">Pending</option>
                        <option value="Accepted">Accepted</option>
                        <option value="Completed">Completed</option>
                        <option value="Cancelled">Cancelled</option>
                      </select>
                    </td>
                    <td class="btn-print"><a href="/dashboard/bill/${order.id}/">${btnPrint}</a></td>
                  </tr>
                `
      contentTable.innerHTML += content
    })

    //--------------------------------------------------------
    const mySelect = document.getElementsByClassName("mySelect")
    showStatus(arrayList, mySelect)
    editStatus(arrayList, mySelect, contentTable)

    /*  ============================ Show Sub-Order Dashboard==============================   */
    var dashboardTrans = document.getElementsByClassName("dashboard-transaction")
    for (let i = 0; i < dashboardTrans.length; i++) {
      dashboardTrans[i].addEventListener('click', function(){

        const exampleModalLabel = document.getElementById("exampleModalLabel")
        exampleModalLabel.innerHTML = `Thông tin chi tiết`

        const tableHeader = document.getElementById("table-header")
        tableHeader.innerHTML = ` <tr>
                                    <th scope="col">STT</th>
                                    <th scope="col">Sản phẩm</th>
                                    <th scope="col">Màu</th>
                                    <th scope="col">Đơn giá</th>
                                    <th scope="col">Số lượng</th>
                                    <th scope="col">Thành tiền</th>
                                  </tr>
                                `
        
        var modalItem = document.querySelector(".modal__item")
        modalItem.innerHTML = ""
        var arrayItem = arrayList[i]
        var orderItems = arrayList[i].orderitem
        var orderitem = detailOrder(orderItems, arrayItem)
        var modalItem = document.querySelector(".modal__item")
        modalItem.innerHTML += orderitem
      })
    }
  
  })
}
  
function detailOrder(orderItems, arrayItem){

  var countItem = 0 
  var item = ""
  var orderListItem = ""
  var totalPerItem = 0
  var totalAllItem = 0
  var totalQuantity = 0

  for (let i = 0; i < orderItems.length; i++) {
    countItem = (i + 1)
    pricePerItem = parseFloat(orderItems[i].price) / parseFloat(orderItems[i].quantity)
    item = ` <tr>
              <th scope="row">${countItem}</th>
              <td>${orderItems[i].product_name}</td>
              <td>${orderItems[i].color}</td>
              <td>${pricePerItem}</td>
              <td>${orderItems[i].quantity}</td>
              <td>${orderItems[i].price}</td>
            </tr>
          `
    orderListItem += item
    totalAllItem += parseInt(orderItems[i].price, 10)
    
    totalQuantity += orderItems[i].quantity
  }
  var totalRow = `  <tr class="total-row">
                      <th scope="row">${countItem + 1}</th>
                      <th colspan="3">Tổng</th>
                      <th>${totalQuantity}</th>
                      <th colspan="1">${totalAllItem}</th>
                    </tr>
                  `
  var note = `<div>
                <strong>Ghi chú: </strong> ${arrayItem.note}
              </div>
              `
  text = orderListItem + totalRow + note
  return text
}

function showStatus(arrayList, mySelect){
  arrayList.forEach(function(arrayItem, index){
    mySelect[index].value = `${arrayItem.status}`
    
  })
}

function editStatus(arrayList, mySelect, contentTable) {
  for (let i = 0; i < mySelect.length; i++) {
    mySelect[i].addEventListener("change", () => {
      const status = mySelect[i].value  
      var idItem = arrayList[i].id
      var urlUpdate = `http://127.0.0.1:8000/api/orders/${idItem}/`
      fetch(urlUpdate, {
        method:'PUT',
        headers: {
          'Content-type':'application/json',
          'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'status': status},{'orderitem':mySelect[i].orderitem}, {'customer': mySelect[i].customer } )
      }).then(function(res) {
        buildDashboard()
      })
    })
  }
}

function urlSearch() {
  const searchOrder = document.getElementById("search-order")
  searchOrder.addEventListener("keyup", function() {
    if (event.keyCode === 13) {
      event.preventDefault()
      location.replace("?search=" + encodeURI(searchOrder.value))
    }
  })
}