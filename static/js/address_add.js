window.onload = function () {


  $("button[name='submit']").click(function (event) {
    // 阻止按钮默认行为，以ajax走信息
    event.preventDefault();

    let receiver_name = $("input[name='receiver_name']").val();
    let receiver_phone = $("input[name='receiver_phone']").val();
    let province = $("#province").val();      // 获取省份值
    let city = $("#city").val();              // 获取城市值
    let district = $("#district").val();      // 获取区县值
    let detailed_address = $("input[name='detailed_address']").val();
    let is_default = $("input[name='is_default']").is(':checked') ? 1 : 0;
    let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();

    $.ajax('/accounts/address/add', {
      method: 'POST',
      data: {
        receiver_name,
        receiver_phone,
        province,
        city,
        district,
        detailed_address,
        is_default,
        csrfmiddlewaretoken
      },
      success: function (result) {
        if (result['code'] === 200) {
          // 获取博客id
          let userAddress_id = result['data']['userAddress_id'];
          // 跳转到博客详情页面
          // window.location = '/accounts/address/' + userAddress_id;
          window.location = '/accounts/address_list'
          return false
        } else {
          alert(result['message']);
        }
      }
    })
  })
}