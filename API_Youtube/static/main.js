console.log('hello')

const spinnerBox = document.getElementById('spinner-box')
const dataBox = document.getElementById('data-box')

// console.log(spinnerBox)
// console.log(dataBox)

$.ajax({
    type: 'GET',
    url: '/new/',
    success: function(response) {
        spinnerBox.classList.add('not-visible')
        console.log(response)
    },
    error: function(error) {
        console.log(error)
    }
})