# Stage 1: Build Environment (Heavy SDK)
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build-env
WORKDIR /app

# Copy all files from the local directory to the container
COPY . ./

# Restore package dependencies and compile the application in Release mode
RUN dotnet restore
RUN dotnet publish -c Release -o out

# Stage 2: Production Environment (Lightweight Runtime)
FROM mcr.microsoft.com/dotnet/aspnet:10.0
WORKDIR /app

# Copy ONLY the compiled .dll files from the 'build-env' stage
COPY --from=build-env /app/out .

# Expose port 8080 (the port our minimal API is listening on)
EXPOSE 8080

# Command to run the application
ENTRYPOINT ["dotnet", "auth-service.dll"]