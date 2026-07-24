using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// The secret key for JWT signature. In production, this should be stored securely (e.g., in .env)
// The key must be at least 32 characters long for the security algorithm to work.
var secureKey = Environment.GetEnvironmentVariable("JWT_SECRET_KEY");
if (string.IsNullOrEmpty(secureKey))
{
    throw new Exception("JWT_SECRET_KEY environment variable is not set!");
}


app.MapPost("/api/auth/login", (LoginRequest request) =>
{
    // Hardcoded credentials for testing purposes.
    // In the next phases, this will be fetched from the C# dedicated database.
    if (request.Email == "admin@example.com" && request.Password == "123456")
    {
        var tokenHandler = new JwtSecurityTokenHandler();
        var key = Encoding.ASCII.GetBytes(secureKey);
        
        // JWT Token configuration
        var tokenDescriptor = new SecurityTokenDescriptor
        {
            // Include user email in the token payload
            Subject = new ClaimsIdentity(new[] { new Claim(ClaimTypes.Email, request.Email) }),
            
            // Token expires after 5 hour
            Expires = DateTime.UtcNow.AddHours(5),
            
            // Sign the token using the secret key
            SigningCredentials = new SigningCredentials(new SymmetricSecurityKey(key), SecurityAlgorithms.HmacSha256Signature)
        };
        
        var token = tokenHandler.CreateToken(tokenDescriptor);
        var jwtString = tokenHandler.WriteToken(token);
        
        return Results.Ok(new { Token = jwtString });
    }

    // Return 401 Unauthorized if credentials are wrong
    return Results.Unauthorized();
});

// Ensure the app listens on all interfaces, which is crucial for Docker networking
app.Run("http://0.0.0.0:8080"); 

// Simple class to bind the incoming JSON request
public class LoginRequest
{
    public string Email { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
}