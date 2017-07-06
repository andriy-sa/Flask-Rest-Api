var app = new Vue({
  el: '#app',
  delimiters: ['@{', '}'],
  data: {
    message: 'Hello Vue!',
    textList: [
      { text: 'Vegetables' },
      { text: 'Cheese' },
      { text: 'Whatever else humans are supposed to eat' }
    ]
  }
});
