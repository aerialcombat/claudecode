// Simple greeting function
function greet(name = 'World') {
  return `Hello, ${name}!`;
}

// Example usage
console.log(greet());
console.log(greet('Claude'));

module.exports = { greet };
